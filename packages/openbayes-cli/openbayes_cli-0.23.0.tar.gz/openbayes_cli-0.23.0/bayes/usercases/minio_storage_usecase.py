import hashlib
import os
import time
from typing import Optional, Callable, Any, Tuple
import threading
from pathlib import Path

import boto3
from botocore.config import Config as BotoCoreConfig
from botocore.exceptions import ClientError, EndpointConnectionError, ConnectionClosedError, ReadTimeoutError
from boto3.s3.transfer import TransferConfig, S3UploadFailedError
from rich import filesize
from tqdm import tqdm

from bayes.client import minio_storage_client
from bayes.client.base import BayesGQLClient
from bayes.model.file.settings import BayesEnvConfig, BayesSettings
from bayes.usercases import dataset_usecase
from bayes.usercases.disk_usecase import IgnoreService, DiskService
from bayes.model.file.openbayes_ignore import IGNORE_FILE_NAME, IGNORE_CLEANUPS, OpenBayesIgnoreSettings
from bayes.usercases.upload_state_manager import UploadStateManager

# 分块上传阈值（8MB）
MULTIPART_THRESHOLD_BYTES = 8 * 1024 * 1024

# S3/MinIO Multipart Upload 关键限制（与 AWS S3 兼容）
# - 单次 Multipart Upload 最多 10,000 个分片
# - 每个分片大小：5MiB ~ 5GiB（最后一个分片无最小限制，但最大仍受 5GiB 约束）
MAX_MULTIPART_PARTS = 10000
MIN_MULTIPART_PART_SIZE_BYTES = 5 * 1024 * 1024
MAX_MULTIPART_PART_SIZE_BYTES = 5 * 1024 * 1024 * 1024


# 网关可能对“单次请求体大小”有限制，会导致 UploadPart 报错：413 Request Entity Too Large。
# 为降低该类错误概率，客户端侧对分片大小做一个“最大值”限制。
# 可通过环境变量 BAYES_MULTIPART_MAX_PART_SIZE_MIB 覆盖（单位：MiB）。
# 注意：这里的单位是 MiB（1 MiB = 1024 * 1024 bytes），不是十进制 MB。
DEFAULT_MAX_PART_SIZE_MIB = 100
DEFAULT_MULTIPART_TARGET_PARTS = 8


def _get_multipart_target_parts() -> int:
    """获取“自适应分片”目标分片数。

    作用：
    - 当文件较小（file_size < max_part_size）时，我们会把 part_size 调小，让分片数量接近该目标值，
      从而提升断点续传的颗粒度（中断后需要重传的数据更少）。

    环境变量：
    - BAYES_MULTIPART_TARGET_PARTS：目标分片数，默认 8

    保护：
    - 解析失败或 <=0：回退默认值
    - 过大：做上限限制，避免产生过多分片导致性能下降或接近 10,000 的协议上限
    """
    raw = os.getenv("BAYES_MULTIPART_TARGET_PARTS", str(DEFAULT_MULTIPART_TARGET_PARTS))
    try:
        n = int(raw)
    except Exception:
        n = DEFAULT_MULTIPART_TARGET_PARTS
    if n <= 0:
        n = DEFAULT_MULTIPART_TARGET_PARTS
    # 合理上限：不追求极端细粒度；过大只会增加请求次数/状态写入频率
    return min(n, 1024)


def _get_max_multipart_part_size_bytes() -> int:
    """获取客户端侧允许的最大分片大小（字节）。

    说明：
    - 这是“客户端侧的分片大小上限”，主要用于规避某些网关对单次请求体大小的限制（413）。
    - 但 S3/MinIO 对 multipart 的**单个分片**有协议下限：5MiB（最后一片例外）。
      所以当用户把环境变量设得小于 5MiB 时，这里会自动抬升到 5MiB，避免出现“上限 < 协议下限”的矛盾。
    """
    raw = os.getenv("BAYES_MULTIPART_MAX_PART_SIZE_MB", str(DEFAULT_MAX_PART_SIZE_MIB))
    try:
        mb = int(raw)
    except Exception:
        mb = DEFAULT_MAX_PART_SIZE_MIB
    if mb <= 0:
        mb = DEFAULT_MAX_PART_SIZE_MIB
    size = mb * 1024 * 1024
    # S3/MinIO multipart 分片最小值约束（最后一片除外，但我们这里把“上限”也抬到最小值，语义更一致）
    if size < MIN_MULTIPART_PART_SIZE_BYTES:
        size = MIN_MULTIPART_PART_SIZE_BYTES
    # 仍需遵守协议上限（5GiB）
    return min(size, MAX_MULTIPART_PART_SIZE_BYTES)

# 分块上传配置（大于 8MB 开启分块）
transfer_config = TransferConfig(multipart_threshold=MULTIPART_THRESHOLD_BYTES, max_concurrency=5)

# 兼容不同版本的 rich：部分版本没有 rich.filesize.binary()
def _format_bytes_binary(num_bytes: int) -> str:
    """用 1024 进位格式化字节数，输出 KiB/MiB/GiB/TiB 等（更贴近 S3 的 5MiB/5GiB 概念）。"""
    try:
        n = float(num_bytes)
    except Exception:
        return str(num_bytes)
    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    i = 0
    while n >= 1024.0 and i < len(units) - 1:
        n /= 1024.0
        i += 1
    if i == 0:
        return f"{int(n)} {units[i]}"
    return f"{n:.1f} {units[i]}"


# 创建一个进度条回调类
class ProgressPercentage:
    def __init__(self, filename, start_bytes=0):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = start_bytes
        self._lock = threading.Lock()
        self.progress_bar = tqdm(
            total=self._size, 
            unit='B', 
            unit_scale=True, 
            desc=os.path.basename(filename),
            initial=start_bytes  # 从已上传的字节数开始
        )

    def __call__(self, bytes_amount):
        # 当回调被调用时，更新进度条
        with self._lock:
            self._seen_so_far += bytes_amount
            self.progress_bar.update(bytes_amount)
            if self._seen_so_far >= self._size:
                self.progress_bar.close()

# 维护 s3 客户端到会话的映射，便于在通用函数中获取到会话进行刷新
_S3_CLIENT_TO_SESSION = {}


def _build_s3_client(endpoint: str, access_key: str, secret_key: str):
    # 开启 botocore 自带的重试（自适应）作为底层兜底，应用层仍会再做显式重试
    # 重要：为避免网络抖动/链接半断时“无限等待”，显式设置超时。
    # connect_timeout：建立连接的最长等待
    # read_timeout：等待服务端响应的最长等待（上传分片后服务端返回 ETag）
    config = BotoCoreConfig(
        retries={"max_attempts": 10, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=900,
    )
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=config,
    )


def _unwrap_client_error(e: Exception) -> Tuple[Optional[ClientError], Exception]:
    # boto3 小文件 upload_file 失败常抛 S3UploadFailedError，内部包裹 ClientError
    if isinstance(e, S3UploadFailedError) and hasattr(e, "original_error"):
        orig = getattr(e, "original_error")
        if isinstance(orig, ClientError):
            return orig, e
    if isinstance(e, ClientError):
        return e, e
    return None, e


def _is_auth_related_error(e: Exception) -> bool:
    ce, _ = _unwrap_client_error(e)
    if ce is None:
        return False
    # 仅将明确的认证/签名/凭证相关错误视为需要刷新；
    # 注意：对象不存在的 404（如 NoSuchKey）不应触发刷新，否则会在每个新文件上反复刷新导致凭证抖动
    code = ce.response.get("Error", {}).get("Code", "")
    if code in {
        "AccessDenied",
        "SignatureDoesNotMatch",
        "InvalidAccessKeyId",
        "ExpiredToken",
        "InvalidToken",
        "NoSuchBucket",
        "NoSuchUpload",
        # 可按需补充与认证直接相关的错误码
    }:
        return True
    return False


def _is_transient_error(e: Exception) -> bool:
    # 网络/临时性错误（包括 5xx）
    if isinstance(e, (EndpointConnectionError, ConnectionClosedError, ReadTimeoutError)):
        return True
    ce, _ = _unwrap_client_error(e)
    if ce is not None:
        status = ce.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status and 500 <= int(status) < 600:
            return True
    return False


def _call_with_retry(s3_client, func: Callable[[Any], Any], session=None, max_attempts: int = 5,
                     initial_backoff: float = 0.5):
    attempt = 0
    last_exception = None
    while attempt < max_attempts:
        try:
            return func(s3_client)
        except Exception as e:  # noqa: B902 - 捕获 boto3/网络相关异常
            last_exception = e
            should_refresh = session is not None and _is_auth_related_error(e)
            should_retry = _is_transient_error(e) or should_refresh
            if not should_retry:
                break
            # 刷新凭证（若需要）
            if should_refresh and session is not None:
                try:
                    old_client_id = id(session.s3_client)
                    session.refresh()
                    s3_client = session.s3_client
                    # 更新映射
                    _S3_CLIENT_TO_SESSION.pop(old_client_id, None)
                    _S3_CLIENT_TO_SESSION[id(s3_client)] = session
                except Exception:
                    # 刷新失败直接继续退避重试
                    pass
            # 退避
            sleep_s = initial_backoff * (2 ** attempt)
            time.sleep(min(sleep_s, 8.0))
            attempt += 1
            continue
    raise last_exception if last_exception else RuntimeError("Unknown error without exception")


class UploadSession:
    """封装一次上传会话，支持凭证刷新与 s3 客户端重建。"""

    def __init__(self, party_name: str, dataset_id: str, version: int, directory: str):
        self.party_name = party_name
        self.dataset_id = dataset_id
        self.version = version
        self.directory = directory
        self.policy = None
        self.s3_client = None
        self.bucket_name = ""
        self.minio_path = ""
        self._last_refresh_time = 0.0
        self.refresh()

    def refresh(self):
        self.policy = get_datasetVersion_upload_policy(
            self.party_name, self.dataset_id, self.version, self.directory
        )
        self.s3_client = _build_s3_client(
            self.policy.endpoint, self.policy.accessKey, self.policy.secretKey
        )
        self.bucket_name, self.minio_path = extract_bucket_and_path(self.policy.path)
        self._last_refresh_time = time.time()
        _S3_CLIENT_TO_SESSION[id(self.s3_client)] = self

def get_datasetVersion_upload_policy(party_name:str, datasetId:str, version:int, key:str):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)

    # api server 的接口会对 key 进行相关的校验
    return minio_storage_client.get_datasetVersion_upload_policy(
        gql_client, party_name, datasetId, version, key
    )


def upload(party_name:str, datasetId:str, abs_dataset_path:str, version:int, directory:str):
    try:
        print(f"正在准备上传数据集 {datasetId}...")

        print("正在获取上传授权...")
        session = UploadSession(party_name, datasetId, version, directory)
        s3_client = session.s3_client
        bucket_name, minio_path = session.bucket_name, session.minio_path
        
        # 检查路径是文件还是目录
        is_file = os.path.isfile(abs_dataset_path)
        
        if is_file:
            # 上传单个文件
            print(f"开始上传文件: {os.path.basename(abs_dataset_path)}")
            
            # 构建远程文件路径
            file_name = os.path.basename(abs_dataset_path)
            remote_file_path = f"{minio_path}/{file_name}".replace("\\", "/")
            
            # 使用支持断点续传的上传函数
            result = upload_file_with_resume(s3_client, bucket_name, abs_dataset_path, remote_file_path, session=session)
            
            if result["success"]:
                if result.get("skipped", False):
                    reason = result.get("skipped_reason")
                    if reason:
                        print(f"\n✅ 已跳过上传: {reason}")
                    else:
                        print(f"\n✅ 上传成功! 文件已存在，已跳过上传")
                else:
                    print(f"\n✅ 上传成功!")
                print(f"数据集 {datasetId} 的版本 v{version} 已更新")
                return True
            else:
                print(f"\n❌ 上传失败: {result.get('error', '未知错误')}")
                return False
        else:
            # 上传文件夹
            print(f"开始上传文件，请耐心等待...")
            file_count = count_files(abs_dataset_path)
            print(f"共发现 {file_count} 个文件")
            
            result = upload_folder(s3_client, bucket_name, abs_dataset_path, minio_path, session=session)
            
            if result["success"]:
                print(f"\n✅ 上传成功! 已上传 {result['uploaded']} 个文件，跳过 {result['skipped']} 个已存在文件")
                print(f"数据集 {datasetId} 的版本 v{version} 已更新")
                return True
            else:
                print(f"\n❌ 上传过程中出现错误: {result['error']}")
                print(f"已上传 {result['uploaded']} 个文件，{result['failed']} 个文件上传失败")
                return False
            
    except Exception as e:
        print(f"\n❌ 上传失败: {str(e)}")
        return False


def count_files(directory):
    """计算目录中的文件总数"""
    count = 0
    for _, _, files in os.walk(directory):
        count += len(files)
    return count


def get_md5(file_path):
    """计算文件 MD5 哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_exists_in_s3(s3_client, bucket, key, local_file_path):
    """检查 MinIO 中是否已经存在相同的文件（通过文件大小 & MD5 校验）"""
    try:
        # 尝试获取会话，以便在头部请求失败时做刷新/重试
        session = _S3_CLIENT_TO_SESSION.get(id(s3_client))
        response = _call_with_retry(
            s3_client,
            lambda c: c.head_object(Bucket=bucket, Key=key),
            session=session,
        )
        remote_size = response["ContentLength"]
        remote_etag = response.get("ETag", "").strip('"')
        
        # 获取本地文件大小
        local_size = os.path.getsize(local_file_path)
        
        # 如果文件大小不同，则肯定不是同一个文件
        if local_size != remote_size:
            return False
            
        # 检查 ETag 是否为多部分上传格式（包含连字符）
        if "-" in remote_etag:
            # 对于多部分上传的文件，仅比较文件大小
            # 或者可以实现更复杂的分块 MD5 计算（如下注释部分）
            return True
        else:
            # 对于小文件，直接比较 MD5
            local_md5 = get_md5(local_file_path)
            return local_md5 == remote_etag
            
    except ClientError:
        return False  # 文件不存在
    except Exception:
        return False


def upload_folder(s3_client, bucket_name, local_folder, remote_folder, session=None):
    """递归上传整个文件夹（保留目录结构 & 断点续传 & 忽略文件）"""
    results = {
        "success": True,
        "uploaded": 0,
        "skipped": 0,
        "failed": 0,
        "ignored": 0,
        "error": None
    }
    
    try:
        # 仅在目录可写且 .openbayesignore 不存在时创建默认文件；
        # 如果是只读或文件不存在，则不创建，忽略逻辑退化为仅使用内置清单
        ignore_file_path = Path(local_folder) / IGNORE_FILE_NAME
        if not ignore_file_path.exists():
            # 判断目录是否可写
            if os.access(local_folder, os.W_OK):
                try:
                    template_content = OpenBayesIgnoreSettings.read_template()
                    with open(ignore_file_path, 'w', encoding='utf-8') as f:
                        f.write(template_content)
                except Exception:
                    # 写入失败时，继续走仅使用内置清单的逻辑
                    pass
        ignore_service = IgnoreService(str(ignore_file_path), IGNORE_CLEANUPS)
        disk_service = DiskService(ignore_service)
        
        print(f"正在分析文件列表...")
        
        # 获取被忽略的文件
        ignored_files, ignored_dirs, err = ignore_service.ignored(local_folder)
        if err is not None:
            results["success"] = False
            results["error"] = str(err)
            return results
            
        # 使用 left 方法获取未被忽略的文件列表
        unignored_files, _, err = ignore_service.left(local_folder)
        if err is not None:
            results["success"] = False
            results["error"] = str(err)
            return results
        
        # 计算被忽略的文件数量
        total_files = 0
        for _, _, files in os.walk(local_folder):
            total_files += len(files)
        
        results["ignored"] = total_files - len(unignored_files)
        
        print(f"剔除在 {IGNORE_FILE_NAME} 中忽略的文件及文件夹...")
        print(f"共有文件 {len(unignored_files)} 个需要上传，忽略了 {results['ignored']} 个文件")
        
        # 打印被忽略的文件和目录
        if ignored_files:
            print("\n被忽略的文件列表:")
            for file in ignored_files:
                print(f"  - {file}")
                
        if ignored_dirs:
            print("\n被忽略的目录列表:")
            for dir in ignored_dirs:
                print(f"  - {dir}/")
        
        # 上传未被忽略的文件
        for local_file_path in unignored_files:
            # 计算相对路径
            relative_path = os.path.relpath(local_file_path, local_folder)
            remote_file_path = f"{remote_folder}/{relative_path}".replace("\\", "/")  # 处理 Windows 路径

            # 使用支持断点续传的上传函数
            result = upload_file_with_resume(s3_client, bucket_name, local_file_path, remote_file_path, session=session)
            
            if result["success"]:
                if result.get("skipped", False):
                    results["skipped"] += 1
                else:
                    results["uploaded"] += 1
            else:
                results["failed"] += 1
                results["success"] = False
                if not results["error"]:
                    results["error"] = result.get("error", "未知错误")
        
        return results
    except Exception as e:
        results["success"] = False
        results["error"] = str(e)
        return results
        

def extract_bucket_and_path(path: str):
    path = path.lstrip('/')
    parts = path.split('/', 1)
    return [parts[0], parts[1] if len(parts) > 1 else ""]


def upload_file_with_resume(s3_client, bucket_name, local_file_path, remote_file_path, session=None):
    """使用自实现的断点续传上传文件到MinIO
    
    Args:
        s3_client: boto3 S3客户端
        bucket_name: 目标桶名
        local_file_path: 本地文件路径
        remote_file_path: 远程文件路径
        
    Returns:
        字典，包含上传结果信息
    """
    # 初始化状态管理器
    state_manager = UploadStateManager()
    
    try:
        # 检查文件是否已经上传
        if file_exists_in_s3(s3_client, bucket_name, remote_file_path, local_file_path):
            print(f"↷ 跳过: {local_file_path} (已存在)")
            # 清除可能存在的状态文件
            state_manager.clear_state(local_file_path, bucket_name, remote_file_path)
            return {"success": True, "skipped": True}

        # 获取文件大小
        file_size = os.path.getsize(local_file_path)
        
        # 小文件直接上传（不需要断点续传）
        if file_size < MULTIPART_THRESHOLD_BYTES:  # 小于分块上传阈值的文件
            progress_callback = ProgressPercentage(local_file_path)
            _call_with_retry(
                s3_client,
                lambda c: c.upload_file(
                    local_file_path,
                    bucket_name,
                    remote_file_path,
                    Config=transfer_config,
                    Callback=progress_callback,
                ),
                session=session,
            )
            print(f"↑ 已上传: {local_file_path}")
            return {"success": True, "skipped": False}
        
        # 大文件使用分块上传 + 断点续传
        # 查找之前的上传状态
        state = state_manager.get_state(local_file_path, bucket_name, remote_file_path)
        
        # 设置分块大小（默认最大分片 128MiB，可通过环境变量调整）：
        # - 上限：不超过客户端侧最大值（避免 UploadPart 触发 413 Request Entity Too Large）
        # - 下限：至少 5MiB（S3/MinIO 要求，最后一块除外）
        #
        # 额外策略（提升断点续传的“颗粒度”）：
        # - 当文件本身比较小（例如 < 128MiB）时，如果仍用 128MiB 分片，往往只会产生 1 个分片，
        #   断点续传意义不大（中断后需要重传整个文件）。
        # - 因此这里对“文件较小”的场景做自适应：让分片数量大约在一个目标值附近（默认 8 个左右），
        #   同时保证分片大小仍遵守 [5MiB, max_part_size]。
        max_part_size = _get_max_multipart_part_size_bytes()
        target_parts = _get_multipart_target_parts()
        if file_size < max_part_size:
            # 让 total_parts ≈ target_parts：part_size ≈ ceil(file_size / target_parts)
            adaptive = (file_size + target_parts - 1) // target_parts
            part_size = max(MIN_MULTIPART_PART_SIZE_BYTES, adaptive)
            part_size = min(part_size, max_part_size)
        else:
            part_size = max_part_size
        # part_size 仍需遵守协议上限（5GiB）
        if part_size > MAX_MULTIPART_PART_SIZE_BYTES:
            part_size = MAX_MULTIPART_PART_SIZE_BYTES
        
        # 计算分块数量
        total_parts = (file_size + part_size - 1) // part_size
        if total_parts > MAX_MULTIPART_PARTS:
            # 当 max_part_size 太小导致分片数超过 10000 时，按需求：跳过该文件并继续下一个
            # （对目录上传尤为重要；对单文件上传则表现为本次上传失败/跳过）
            hint = (
                f"文件过大：在最大分片 {filesize.decimal(part_size)} 下需要 {total_parts} 个分片，"
                f"超过上限 {MAX_MULTIPART_PARTS}。"
            )
            hint += " 请考虑拆分文件或适当增大 BAYES_MULTIPART_MAX_PART_SIZE_MB。"
            # 如果之前已有状态（意味着存在未完成的 multipart upload），尽量中止并清理，避免占用资源
            if state and state.get("upload_id"):
                try:
                    _call_with_retry(
                        s3_client,
                        lambda c: c.abort_multipart_upload(
                            Bucket=bucket_name,
                            Key=remote_file_path,
                            UploadId=state["upload_id"],
                        ),
                        session=session,
                    )
                except Exception:
                    pass
            state_manager.clear_state(local_file_path, bucket_name, remote_file_path)
            print(f"↷ 跳过: {local_file_path}（{hint}）")
            return {"success": True, "skipped": True, "skipped_reason": hint}
        
        if state and state.get('upload_id'):
            # 恢复之前的上传
            print(f"找到未完成的上传任务，正在恢复: {os.path.basename(local_file_path)}")
            upload_id = state['upload_id']
            completed_parts = state['parts']
            
            try:
                # 验证上传ID是否仍然有效
                _call_with_retry(
                    s3_client,
                    lambda c: c.list_parts(Bucket=bucket_name, Key=remote_file_path, UploadId=upload_id),
                    session=session,
                )
                print(f"恢复上传ID: {upload_id}")
                # 若状态中记录了历史分片大小，则优先复用，避免分片边界错位
                saved_part_size = state.get('part_size')
                if saved_part_size is not None:
                    # 恢复时必须保持分片大小一致；但如果历史分片大小 > 当前允许的最大分片大小，
                    # 直接恢复会继续触发 413。此时中止旧上传并按新策略重启（或跳过）。
                    saved_part_size_int = int(saved_part_size)
                    if saved_part_size_int > _get_max_multipart_part_size_bytes():
                        print("历史分块大小超过当前允许的最大分片大小，正在中止旧上传并按新分片策略重启...")
                        try:
                            _call_with_retry(
                                s3_client,
                                lambda c: c.abort_multipart_upload(
                                    Bucket=bucket_name,
                                    Key=remote_file_path,
                                    UploadId=upload_id,
                                ),
                                session=session,
                            )
                        except Exception:
                            pass
                        state_manager.clear_state(local_file_path, bucket_name, remote_file_path)
                        # 重新计算 part_size/total_parts（会走上面的分片数检查，必要时跳过）
                        max_part_size = _get_max_multipart_part_size_bytes()
                        part_size = max(MIN_MULTIPART_PART_SIZE_BYTES, max_part_size)
                        if part_size > MAX_MULTIPART_PART_SIZE_BYTES:
                            part_size = MAX_MULTIPART_PART_SIZE_BYTES
                        total_parts = (file_size + part_size - 1) // part_size
                        if total_parts > MAX_MULTIPART_PARTS:
                            hint = (
                                f"文件过大：在最大分片 {filesize.decimal(part_size)} 下需要 {total_parts} 个分片，"
                                f"超过上限 {MAX_MULTIPART_PARTS}。"
                            )
                            hint += " 请考虑拆分文件或适当增大 BAYES_MULTIPART_MAX_PART_SIZE_MB。"
                            print(f"↷ 跳过: {local_file_path}（{hint}）")
                            return {"success": True, "skipped": True, "skipped_reason": hint}
                        print(f"开始新的分块上传: {os.path.basename(local_file_path)}")
                        response = _call_with_retry(
                            s3_client,
                            lambda c: c.create_multipart_upload(Bucket=bucket_name, Key=remote_file_path),
                            session=session,
                        )
                        upload_id = response["UploadId"]
                        completed_parts = []
                        state_manager.save_state(
                            local_file_path, bucket_name, remote_file_path,
                            upload_id, completed_parts, part_size=part_size
                        )
                        print(f"创建新的上传ID: {upload_id}")
                    else:
                        part_size = max(MIN_MULTIPART_PART_SIZE_BYTES, saved_part_size_int)
                    total_parts = (file_size + part_size - 1) // part_size
                    print(f"按历史分块大小恢复: {filesize.decimal(part_size)}，共 {total_parts} 个分块")
                    # 如果历史分片大小导致总分片数仍然超过上限，则中止旧上传并重新创建
                    if total_parts > MAX_MULTIPART_PARTS:
                        print("历史分块大小会导致分片数超过 10000，上限受限。正在中止旧上传并重启以增大分块大小...")
                        try:
                            _call_with_retry(
                                s3_client,
                                lambda c: c.abort_multipart_upload(
                                    Bucket=bucket_name,
                                    Key=remote_file_path,
                                    UploadId=upload_id,
                                ),
                                session=session,
                            )
                        except Exception:
                            # 忽略中止异常，继续重启
                            pass
                        state_manager.clear_state(local_file_path, bucket_name, remote_file_path)
                        # 按新的分片策略重启（仍会执行分片数上限检查，必要时跳过）
                        max_part_size = _get_max_multipart_part_size_bytes()
                        part_size = max(MIN_MULTIPART_PART_SIZE_BYTES, max_part_size)
                        if part_size > MAX_MULTIPART_PART_SIZE_BYTES:
                            part_size = MAX_MULTIPART_PART_SIZE_BYTES
                        total_parts = (file_size + part_size - 1) // part_size
                        if total_parts > MAX_MULTIPART_PARTS:
                            hint = (
                                f"文件过大：在最大分片 {filesize.decimal(part_size)} 下需要 {total_parts} 个分片，"
                                f"超过上限 {MAX_MULTIPART_PARTS}。"
                            )
                            hint += " 请考虑拆分文件或适当增大 BAYES_MULTIPART_MAX_PART_SIZE_MB。"
                            print(f"↷ 跳过: {local_file_path}（{hint}）")
                            return {"success": True, "skipped": True, "skipped_reason": hint}
                        print(f"开始新的分块上传: {os.path.basename(local_file_path)}")
                        response = _call_with_retry(
                            s3_client,
                            lambda c: c.create_multipart_upload(Bucket=bucket_name, Key=remote_file_path),
                            session=session,
                        )
                        upload_id = response['UploadId']
                        completed_parts = []
                        state_manager.save_state(
                            local_file_path, bucket_name, remote_file_path,
                            upload_id, completed_parts, part_size=part_size
                        )
                        print(f"创建新的上传ID: {upload_id}")
                else:
                    # 旧版本状态文件无法确定历史分片大小，安全起见中止旧上传并重启
                    print("检测到旧版上传状态（缺少分片大小），为避免分片错位，正在中止旧上传并重启...")
                    try:
                        _call_with_retry(
                            s3_client,
                            lambda c: c.abort_multipart_upload(
                                Bucket=bucket_name,
                                Key=remote_file_path,
                                UploadId=upload_id,
                            ),
                            session=session,
                        )
                    except Exception:
                        pass
                    state_manager.clear_state(local_file_path, bucket_name, remote_file_path)
                    # 重新开始新的上传
                    max_part_size = _get_max_multipart_part_size_bytes()
                    part_size = max(MIN_MULTIPART_PART_SIZE_BYTES, max_part_size)
                    if part_size > MAX_MULTIPART_PART_SIZE_BYTES:
                        part_size = MAX_MULTIPART_PART_SIZE_BYTES
                    total_parts = (file_size + part_size - 1) // part_size
                    if total_parts > MAX_MULTIPART_PARTS:
                        hint = (
                            f"文件过大：在最大分片 {filesize.decimal(part_size)} 下需要 {total_parts} 个分片，"
                            f"超过上限 {MAX_MULTIPART_PARTS}。"
                        )
                        hint += " 请考虑拆分文件上传"
                        print(f"↷ 跳过: {local_file_path}（{hint}）")
                        return {"success": True, "skipped": True, "skipped_reason": hint}
                    print(f"开始新的分块上传: {os.path.basename(local_file_path)}")
                    response = _call_with_retry(
                        s3_client,
                        lambda c: c.create_multipart_upload(Bucket=bucket_name, Key=remote_file_path),
                        session=session,
                    )
                    upload_id = response['UploadId']
                    completed_parts = []
                    state_manager.save_state(
                        local_file_path, bucket_name, remote_file_path,
                        upload_id, completed_parts, part_size=part_size
                    )
                    print(f"创建新的上传ID: {upload_id}")
                print(f"已上传 {len(completed_parts)} 个分块，共 {total_parts} 个分块")
            except Exception as e:
                # 上传ID无效，需要重新开始
                print(f"无法恢复之前的上传: {e}")
                state = None
                completed_parts = []
        else:
            # 开始新的上传
            print(f"开始新的分块上传: {os.path.basename(local_file_path)}")
            response = _call_with_retry(
                s3_client,
                lambda c: c.create_multipart_upload(Bucket=bucket_name, Key=remote_file_path),
                session=session,
            )
            upload_id = response['UploadId']
            completed_parts = []
            # 保存初始状态
            state_manager.save_state(
                local_file_path, bucket_name, remote_file_path, 
                upload_id, completed_parts, part_size=part_size
            )
            print(f"创建新的上传ID: {upload_id}")
        
        # 计算已完成的字节数
        completed_bytes = 0
        for part in completed_parts:
            part_num = part['PartNumber']
            # 估算完成的字节数
            if part_num < total_parts:
                completed_bytes += part_size
            else:
                completed_bytes += file_size % part_size or part_size
        
        # 创建进度条，直接设置初始值为已完成字节数
        progress = tqdm(
            total=file_size,
            unit='B',
            unit_scale=True,
            desc=os.path.basename(local_file_path),
            initial=completed_bytes  # 关键修改：设置初始值
        )
        
        # 已上传分块的编号集合
        uploaded_part_numbers = {part['PartNumber'] for part in completed_parts}
        
        try:
            # 打开文件
            with open(local_file_path, 'rb') as f:
                # 上传每个分块
                for part_num in range(1, total_parts + 1):
                    # 如果该分块已上传，跳过
                    if part_num in uploaded_part_numbers:
                        continue
                    
                    # 定位到正确的文件位置
                    f.seek((part_num - 1) * part_size)
                    
                    # 读取当前分块
                    if part_num == total_parts:
                        # 最后一个分块可能较小
                        data = f.read(file_size - (part_num - 1) * part_size)
                    else:
                        data = f.read(part_size)
                    
                    # 上传分块
                    # 进度条不动时，通常卡在“某个分块的网络请求”或“最终合并分块”；
                    # 给用户一个明确的当前分块提示，便于判断是否真的在工作。
                    try:
                        progress.set_postfix_str(f"part {part_num}/{total_parts}")
                    except Exception:
                        # tqdm 在某些环境可能不支持 set_postfix_str，忽略即可
                        pass
                    response = _call_with_retry(
                        s3_client,
                        lambda c: c.upload_part(
                            Bucket=bucket_name,
                            Key=remote_file_path,
                            PartNumber=part_num,
                            UploadId=upload_id,
                            Body=data,
                        ),
                        session=session,
                    )
                    
                    # 记录已上传的分块
                    etag = response['ETag']
                    completed_parts.append({
                        'PartNumber': part_num,
                        'ETag': etag
                    })
                    
                    # 更新进度条
                    progress.update(len(data))
                    
                    # 保存上传状态（记录分片大小，保证可恢复性）
                    state_manager.save_state(
                        local_file_path, bucket_name, remote_file_path,
                        upload_id, completed_parts, part_size=part_size
                    )
            
            # 完成分块上传
            print("\n所有分块已上传，正在请求服务端完成合并。")
            print(
                f"提示：这个步骤不会增加上传字节数，所以进度条可能看起来“不动”。"
                f"服务端会进行对象完成/元数据写入与校验。"
                f"（本次分片数：{total_parts}，分片大小：{_format_bytes_binary(part_size)}，约 {filesize.decimal(part_size)}）"
            )
            completed_parts.sort(key=lambda x: x['PartNumber'])
            _call_with_retry(
                s3_client,
                lambda c: c.complete_multipart_upload(
                    Bucket=bucket_name,
                    Key=remote_file_path,
                    UploadId=upload_id,
                    MultipartUpload={'Parts': completed_parts},
                ),
                session=session,
            )
            
            # 关闭进度条
            progress.close()
            
            # 清除状态文件
            state_manager.clear_state(local_file_path, bucket_name, remote_file_path)
            
            print(f"↑ 已上传: {local_file_path}")
            return {"success": True, "skipped": False}
            
        except KeyboardInterrupt:
            # 用户中断，保存当前状态
            progress.close()
            print(f"\n上传已暂停: {local_file_path}")
            print(f"上传进度已保存，下次运行时将继续上传")
            return {"success": False, "error": "用户中断"}
            
        except Exception as e:
            # 其他错误
            progress.close()
            print(f"✗ 上传出错: {local_file_path} - {str(e)}")
            return {"success": False, "error": str(e)}
            
    except Exception as e:
        print(f"✗ 上传失败: {local_file_path} - {str(e)}")
        return {"success": False, "error": str(e)}


def upload_file(s3_client, bucket_name, local_file_path, remote_file_path):
    return upload_file_with_resume(s3_client, bucket_name, local_file_path, remote_file_path)


def upload_source_code(party_name: str, source_code_path: str, storageType: str):
    try:
        print(f"正在准备上传源代码...")
        print("正在获取上传授权...")
        policy = get_source_code_upload_policy(party_name, storageType)

        s3_client = boto3.client(
            "s3",
            endpoint_url=policy.endpoint,
            aws_access_key_id=policy.accessKey,
            aws_secret_access_key=policy.secretKey
        )
        
        bucket_name, minio_path = extract_bucket_and_path(policy.path)
        
        # Check if source_code_path exists
        if not os.path.exists(source_code_path):
            print(f"❌ 路径不存在: {source_code_path}")
            return None
            
        print(f"开始扫描文件，请稍候...")
        
        # Get all files in the directory and subdirectories
        all_files = []
        total_size = 0
        for root, _, files in os.walk(source_code_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                all_files.append((file_path, file_size))
                total_size += file_size
        
        total_files = len(all_files)
        print(f"共发现 {total_files} 个文件，总计 {filesize.decimal(total_size)}，开始上传...")
        
        # Create a single progress bar for all files
        with tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc="上传进度"
        ) as overall_progress:
            
            # Upload each file and update the overall progress
            uploaded_count = 0
            failed_count = 0
            
            for local_file_path, file_size in all_files:
                try:
                    # Calculate relative path
                    relative_path = os.path.relpath(local_file_path, source_code_path)
                    remote_file_path = f"{minio_path}/{relative_path}".replace("\\", "/")
                    
                    # Show current file being uploaded (without progress)
                    current_file = os.path.basename(local_file_path)
                    overall_progress.set_description(f"上传: {current_file}")
                    
                    # Define callback for updating overall progress
                    def progress_callback(bytes_amount):
                        overall_progress.update(bytes_amount)
                    
                    # Upload file
                    s3_client.upload_file(
                        local_file_path,
                        bucket_name,
                        remote_file_path,
                        Callback=progress_callback
                    )
                    
                    uploaded_count += 1
                    
                    # Update description to show progress
                    percentage = int((uploaded_count / total_files) * 100)
                    overall_progress.set_description(f"上传进度: {percentage}% ({uploaded_count}/{total_files})")
                    
                except Exception as e:
                    print(f"\n✗ 上传失败: {local_file_path} - {str(e)}")
                    failed_count += 1

        if failed_count == 0:
            print(f"\n✅ 源代码上传成功! 已上传 {uploaded_count} 个文件")
            return policy.id
        else:
            print(f"\n⚠️ 源代码上传部分完成: 成功 {uploaded_count} 个文件，失败 {failed_count} 个文件")
            return None
            
    except Exception as e:
        print(f"\n❌ 上传失败: {str(e)}")
        return None


def get_source_code_upload_policy(party_name: str, storageType: str):
    default_env: Optional[BayesEnvConfig] = BayesSettings().default_env
    gql_client = BayesGQLClient(default_env.graphQL, default_env.token)
    policy = minio_storage_client.get_source_code_upload_policy(gql_client, party_name, storageType)
    return policy