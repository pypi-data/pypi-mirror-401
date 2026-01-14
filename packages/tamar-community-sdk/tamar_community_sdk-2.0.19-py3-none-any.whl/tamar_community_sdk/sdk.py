"""
Tamar Community SDK for Python

支持:
- 文件上传（分片上传、断点续传、文件去重）
- HLS 视频流
- 文件管理
"""
import asyncio
import contextvars
import hashlib
import mimetypes
import os
from pathlib import Path
from typing import Optional, Union, Callable, Awaitable, BinaryIO, List, Dict, Any

import aiohttp
import aiofiles

# 使用 contextvars 存储每个异步上下文的 session，解决并发问题
_context_session: contextvars.ContextVar[Optional[aiohttp.ClientSession]] = contextvars.ContextVar(
    '_context_session', default=None
)

from .types import (
    FileInfo,
    UploadResult,
    UploadOptions,
    ListFilesParams,
    PartInfo,
    ProgressCallback,
    HLSInfo,
    HLSVariant,
    FileField,
    BatchGetFilesResult,
)
from .exceptions import UploadError, AuthError, NetworkError, AbortError


# Token 获取函数类型
TokenGetter = Union[Callable[[], str], Callable[[], Awaitable[str]]]
# 日志回调类型
LogCallback = Callable[[str], None]


class TamarCommunitySDK:
    """
    Tamar Community SDK

    支持文件上传、HLS视频流、文件管理的异步客户端

    Example:
        ```python
        sdk = TamarCommunitySDK(
            base_url="https://api.example.com",
            get_token=lambda: "your-token"
        )

        # 上传文件
        result = await sdk.upload(
            file_path="/path/to/file.mp4",
            options=UploadOptions(
                category="video",
                on_progress=lambda p: print(f"上传进度: {p:.1f}%")
            )
        )
        print(f"上传完成: {result.file.oss_url}")

        # 获取 HLS 信息
        hls_info = await sdk.get_hls_info(result.file.imagekit_url)
        if hls_info.hls_available:
            print(f"HLS 播放地址: {hls_info.master_url}")
        ```
    """

    # 默认分块大小（用于哈希计算）
    HASH_CHUNK_SIZE = 8 * 1024 * 1024  # 8MB

    # 文件类型映射
    FILE_TYPE_MAP = {
        # Video
        ".mp4": {"category": "video", "content_type": "video/mp4"},
        ".m4v": {"category": "video", "content_type": "video/x-m4v"},
        ".mov": {"category": "video", "content_type": "video/quicktime"},
        ".avi": {"category": "video", "content_type": "video/x-msvideo"},
        ".mkv": {"category": "video", "content_type": "video/x-matroska"},
        ".webm": {"category": "video", "content_type": "video/webm"},
        ".flv": {"category": "video", "content_type": "video/x-flv"},
        ".wmv": {"category": "video", "content_type": "video/x-ms-wmv"},
        ".3gp": {"category": "video", "content_type": "video/3gpp"},
        ".3g2": {"category": "video", "content_type": "video/3gpp2"},
        ".mts": {"category": "video", "content_type": "video/mp2t"},
        ".m2ts": {"category": "video", "content_type": "video/mp2t"},
        ".ts": {"category": "video", "content_type": "video/mp2t"},
        ".vob": {"category": "video", "content_type": "video/x-ms-vob"},
        ".ogv": {"category": "video", "content_type": "video/ogg"},
        ".rm": {"category": "video", "content_type": "application/vnd.rn-realmedia"},
        ".rmvb": {"category": "video", "content_type": "application/vnd.rn-realmedia-vbr"},
        ".asf": {"category": "video", "content_type": "video/x-ms-asf"},
        ".divx": {"category": "video", "content_type": "video/x-divx"},
        ".f4v": {"category": "video", "content_type": "video/x-f4v"},
        ".mpg": {"category": "video", "content_type": "video/mpeg"},
        ".mpeg": {"category": "video", "content_type": "video/mpeg"},
        # Image
        ".jpg": {"category": "image", "content_type": "image/jpeg"},
        ".jpeg": {"category": "image", "content_type": "image/jpeg"},
        ".png": {"category": "image", "content_type": "image/png"},
        ".gif": {"category": "image", "content_type": "image/gif"},
        ".webp": {"category": "image", "content_type": "image/webp"},
        ".bmp": {"category": "image", "content_type": "image/bmp"},
        # Audio
        ".mp3": {"category": "audio", "content_type": "audio/mpeg"},
        ".wav": {"category": "audio", "content_type": "audio/wav"},
        ".ogg": {"category": "audio", "content_type": "audio/ogg"},
        ".aac": {"category": "audio", "content_type": "audio/aac"},
        ".flac": {"category": "audio", "content_type": "audio/flac"},
        ".m4a": {"category": "audio", "content_type": "audio/mp4"},
        ".wma": {"category": "audio", "content_type": "audio/x-ms-wma"},
        # Document
        ".pdf": {"category": "document", "content_type": "application/pdf"},
        ".doc": {"category": "document", "content_type": "application/msword"},
        ".docx": {"category": "document", "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
        ".xls": {"category": "document", "content_type": "application/vnd.ms-excel"},
        ".xlsx": {"category": "document", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
        ".ppt": {"category": "document", "content_type": "application/vnd.ms-powerpoint"},
        ".pptx": {"category": "document", "content_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation"},
        ".txt": {"category": "document", "content_type": "text/plain"},
    }

    def __init__(
        self,
        base_url: str,
        get_token: TokenGetter = None,
        api_key: Optional[str] = None,
        concurrency: int = 3,
        retry_count: int = 3,
        retry_delay: float = 1.0,
        timeout: float = 300.0,
        on_log: Optional[LogCallback] = None,
    ):
        """
        初始化 SDK

        Args:
            base_url: API 基础地址
            get_token: 获取认证令牌的函数（支持同步和异步，与 api_key 二选一）
            api_key: API Key（用于内部服务调用，与 get_token 二选一）
            concurrency: 并发上传分片数（默认 3）
            retry_count: 失败重试次数（默认 3）
            retry_delay: 重试延迟秒数（默认 1.0）
            timeout: 请求超时秒数（默认 300）
            on_log: 日志回调函数

        Example:
            # 使用 Token 认证（用户端）
            sdk = TamarCommunitySDK(
                base_url="https://api.example.com",
                get_token=lambda: "your-token"
            )

            # 使用 API Key 认证（服务端）
            sdk = TamarCommunitySDK(
                base_url="https://api.example.com",
                api_key="your-api-key"
            )

            # 上传时指定用户上下文
            result = await sdk.upload(
                file_path="/path/to/file.mp4",
                options=UploadOptions(
                    user_id="user-123",
                    org_id="org-456"
                )
            )
        """
        self.base_url = base_url.rstrip("/")
        self._get_token = get_token
        self._api_key = api_key
        self.concurrency = concurrency
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout
        self._on_log = on_log
        self._session: Optional[aiohttp.ClientSession] = None
        self._cancelled = False

    def _log(self, message: str):
        """输出日志"""
        if self._on_log:
            self._on_log(message)

    async def _get_token_async(self) -> str:
        """异步获取 token"""
        result = self._get_token()
        if asyncio.iscoroutine(result):
            result = await result
        # 自动添加 Bearer 前缀
        if result and not result.startswith("Bearer "):
            result = f"Bearer {result}"
        return result

    async def _get_session(self) -> aiohttp.ClientSession:
        """获取 HTTP 会话

        优先返回当前异步上下文的 session（通过 contextvars 隔离），
        否则返回/创建全局 session。
        """
        # 优先使用当前上下文的 session（线程安全，支持并发）
        ctx_session = _context_session.get()
        if ctx_session is not None and not ctx_session.closed:
            return ctx_session
        # 否则使用全局 session
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self):
        """关闭全局 HTTP 会话

        显式关闭全局 session。通常在应用退出时调用。
        """
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def __aenter__(self):
        """进入异步上下文

        创建独立的 session，存储在 contextvars 中，与其他并发任务隔离。
        每次 async with 都会创建新的 session，退出时自动关闭。
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        session = aiohttp.ClientSession(timeout=timeout)
        _context_session.set(session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """退出异步上下文

        关闭当前上下文的 session，不影响其他并发任务。
        """
        session = _context_session.get()
        if session and not session.closed:
            await session.close()
        _context_session.set(None)

    async def _request(
        self,
        method: str,
        path: str,
        json: dict = None,
        params: dict = None,
        headers: dict = None,
    ) -> dict:
        """发送 API 请求"""
        session = await self._get_session()

        url = f"{self.base_url}{path}"
        req_headers = {
            "Content-Type": "application/json",
        }

        # 支持两种认证方式：API Key 或 Token
        if self._api_key:
            req_headers["X-API-Key"] = self._api_key
        elif self._get_token:
            token = await self._get_token_async()
            req_headers["Authorization"] = token

        if headers:
            req_headers.update(headers)

        for attempt in range(self.retry_count):
            try:
                async with session.request(
                    method,
                    url,
                    json=json,
                    params=params,
                    headers=req_headers,
                ) as response:
                    data = await response.json()

                    if response.status == 401:
                        raise AuthError("认证失败，请检查 token", code=401)

                    if response.status >= 400:
                        error_msg = data.get("message", f"请求失败: {response.status}")
                        raise UploadError(error_msg, code=response.status, details=data)

                    # 检查业务错误码
                    if data.get("code") not in [0, 1000, None]:
                        raise UploadError(
                            data.get("message", "请求失败"),
                            code=data.get("code"),
                            details=data,
                        )

                    return data.get("data", data)

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt < self.retry_count - 1:
                    delay = self.retry_delay * (attempt + 1)
                    self._log(f"请求失败，{delay}s 后重试: {e}")
                    await asyncio.sleep(delay)
                else:
                    raise NetworkError(f"网络请求失败: {e}")

    # ==================== 哈希计算 ====================

    async def calculate_hash(
        self,
        file: Union[str, Path, bytes, BinaryIO],
        on_progress: Optional[ProgressCallback] = None,
    ) -> str:
        """
        计算文件 SHA-256 哈希值

        Args:
            file: 文件路径、字节数据或文件对象
            on_progress: 进度回调 (0-100)

        Returns:
            SHA-256 哈希值（64位小写十六进制）
        """
        sha256_hash = hashlib.sha256()
        total_size = 0
        processed = 0

        # 获取文件大小
        if isinstance(file, (str, Path)):
            total_size = os.path.getsize(file)
        elif isinstance(file, bytes):
            total_size = len(file)
        elif hasattr(file, "seek") and hasattr(file, "read"):
            pos = file.tell()
            file.seek(0, 2)
            total_size = file.tell()
            file.seek(pos)

        async def update_progress():
            if on_progress and total_size > 0:
                percent = (processed / total_size) * 100
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(percent)
                else:
                    on_progress(percent)

        if isinstance(file, (str, Path)):
            # 文件路径
            async with aiofiles.open(file, "rb") as f:
                while True:
                    chunk = await f.read(self.HASH_CHUNK_SIZE)
                    if not chunk:
                        break
                    sha256_hash.update(chunk)
                    processed += len(chunk)
                    await update_progress()

        elif isinstance(file, bytes):
            # 字节数据
            for i in range(0, len(file), self.HASH_CHUNK_SIZE):
                chunk = file[i : i + self.HASH_CHUNK_SIZE]
                sha256_hash.update(chunk)
                processed += len(chunk)
                await update_progress()

        else:
            # 文件对象
            while True:
                chunk = file.read(self.HASH_CHUNK_SIZE)
                if not chunk:
                    break
                if asyncio.iscoroutine(chunk):
                    chunk = await chunk
                sha256_hash.update(chunk)
                processed += len(chunk)
                await update_progress()

        return sha256_hash.hexdigest()

    # ==================== 文件类型 ====================

    @classmethod
    def get_file_type_info(cls, file_name_or_ext: str) -> Dict[str, str]:
        """
        根据文件名或扩展名获取文件类型信息

        Args:
            file_name_or_ext: 文件名或扩展名（如 'video.mp4' 或 'mp4'）

        Returns:
            {"category": "video", "content_type": "video/mp4"}
        """
        if "." in file_name_or_ext:
            ext = "." + file_name_or_ext.rsplit(".", 1)[-1].lower()
        else:
            ext = "." + file_name_or_ext.lower()

        info = cls.FILE_TYPE_MAP.get(ext)
        if info:
            return info

        # 尝试使用 mimetypes
        mime_type = mimetypes.guess_type(f"file{ext}")[0] or "application/octet-stream"
        return {"category": "general", "content_type": mime_type}

    def _get_file_info(
        self, file: Union[str, Path, bytes, BinaryIO], file_name: Optional[str] = None
    ) -> tuple[str, int, str, str]:
        """
        获取文件信息

        Returns:
            (文件名, 文件大小, MIME 类型, 文件扩展名)
        """
        if isinstance(file, (str, Path)):
            path = Path(file)
            name = file_name or path.name
            size = path.stat().st_size
        elif isinstance(file, bytes):
            name = file_name or "file"
            size = len(file)
        else:
            name = file_name or getattr(file, "name", "file")
            pos = file.tell()
            file.seek(0, 2)
            size = file.tell()
            file.seek(pos)

        # 获取文件扩展名和 MIME 类型
        ext = Path(name).suffix.lower().lstrip(".")
        type_info = self.get_file_type_info(ext)

        return name, size, type_info["content_type"], ext

    # ==================== 上传 ====================

    async def upload(
        self,
        file: Union[str, Path, bytes, BinaryIO],
        file_name: Optional[str] = None,
        options: Optional[UploadOptions] = None,
    ) -> UploadResult:
        """
        上传文件

        支持自动 SHA-256 哈希计算、去重、断点续传

        Args:
            file: 文件路径、字节数据或文件对象
            file_name: 文件名（可选，从文件路径自动获取）
            options: 上传选项

        Returns:
            上传结果，包含文件信息（如果命中去重，deduplicated=True）

        Raises:
            UploadError: 上传失败
            AbortError: 上传被取消
        """
        self._cancelled = False
        options = options or UploadOptions()

        # 获取文件信息
        name, size, mime_type, file_ext = self._get_file_info(file, file_name)
        content_type = options.content_type or mime_type

        # 自动检测 category
        if not options.category or options.category == "general":
            type_info = self.get_file_type_info(file_ext)
            category = type_info["category"]
        else:
            category = options.category

        self._log(f"文件名: {name}")
        self._log(f"扩展名: {file_ext}")
        self._log(f"大小: {size} 字节 ({size / 1024 / 1024:.2f} MB)")
        self._log(f"分类: {category}")
        self._log(f"Content-Type: {content_type}")

        # 计算 SHA-256 哈希
        self._log("计算文件 SHA-256...")
        file_hash = await self.calculate_hash(file, options.on_hash_progress)
        self._log(f"SHA-256: {file_hash}")

        if self._cancelled:
            raise AbortError()

        # 初始化上传
        self._log("初始化上传...")

        init_result = await self._init_upload(
            file_ext=file_ext,
            file_size=size,
            file_hash=file_hash,
            category=category,
            content_type=content_type,
            part_size=options.part_size,
            metadata=options.metadata,
            user_id=options.user_id,
            org_id=options.org_id,
        )

        status = init_result.get("status")

        # 去重命中，秒传
        if status == "completed":
            self._log("文件已存在，秒传成功！")
            if options.on_progress:
                if asyncio.iscoroutinefunction(options.on_progress):
                    await options.on_progress(100)
                else:
                    options.on_progress(100)
            return UploadResult.from_dict(init_result.get("file", {}), deduplicated=True)

        if self._cancelled:
            raise AbortError()

        # 需要上传分片
        file_id = init_result.get("file_id")
        parts = [PartInfo.from_dict(p) for p in init_result.get("parts", [])]

        # 过滤出需要上传的分片
        pending_parts = [p for p in parts if not p.uploaded]
        total_parts = len(parts)
        uploaded_count = total_parts - len(pending_parts)

        if status == "resuming":
            self._log(f"断点续传: 已上传 {uploaded_count}/{total_parts} 个分片")
        else:
            self._log(f"新上传: 共 {total_parts} 个分片")

        # 并发上传分片
        await self._upload_parts(
            file=file,
            parts=pending_parts,
            total_parts=total_parts,
            uploaded_count=uploaded_count,
            on_progress=options.on_progress,
        )

        if self._cancelled:
            raise AbortError()

        # 完成上传
        self._log("完成上传...")
        result = await self._complete_upload(file_id, user_id=options.user_id)

        self._log("上传完成！")
        return UploadResult.from_dict(result)

    async def _init_upload(
        self,
        file_ext: str,
        file_size: int,
        file_hash: str,
        category: str = "general",
        content_type: Optional[str] = None,
        part_size: Optional[int] = None,
        metadata: Optional[dict] = None,
        user_id: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> dict:
        """初始化上传"""
        payload = {
            "file_ext": file_ext,
            "file_size": file_size,
            "file_hash": file_hash,
            "category": category,
        }
        if content_type:
            payload["content_type"] = content_type
        if part_size:
            payload["part_size"] = part_size
        if metadata:
            payload["metadata"] = metadata
        if user_id:
            payload["user_id"] = user_id
        if org_id:
            payload["org_id"] = org_id

        return await self._request("POST", "/api/community/files/upload/init", json=payload)

    async def _upload_parts(
        self,
        file: Union[str, Path, bytes, BinaryIO],
        parts: List[PartInfo],
        total_parts: int,
        uploaded_count: int = 0,
        on_progress: Optional[ProgressCallback] = None,
    ):
        """并发上传分片"""
        if not parts:
            return

        session = await self._get_session()
        completed = uploaded_count
        lock = asyncio.Lock()

        async def update_progress():
            if on_progress:
                percent = (completed / total_parts) * 100
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(percent)
                else:
                    on_progress(percent)

        async def upload_part(part: PartInfo):
            nonlocal completed

            if self._cancelled:
                return

            # 读取分片数据
            if isinstance(file, (str, Path)):
                async with aiofiles.open(file, "rb") as f:
                    await f.seek(part.start)
                    data = await f.read(part.size)
            elif isinstance(file, bytes):
                data = file[part.start : part.end]
            else:
                file.seek(part.start)
                data = file.read(part.size)
                if asyncio.iscoroutine(data):
                    data = await data

            # 上传到 OSS
            for attempt in range(self.retry_count):
                if self._cancelled:
                    return

                try:
                    async with session.put(
                        part.upload_url,
                        data=data,
                        skip_auto_headers=["Content-Type"],
                    ) as response:
                        if response.status not in [200, 201]:
                            text = await response.text()
                            raise UploadError(f"分片上传失败: {response.status} - {text}")

                        async with lock:
                            completed += 1
                            await update_progress()
                        return

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    if attempt < self.retry_count - 1:
                        delay = self.retry_delay * (attempt + 1)
                        self._log(f"分片 {part.part_number} 上传失败，{delay}s 后重试: {e}")
                        await asyncio.sleep(delay)
                    else:
                        raise NetworkError(f"分片 {part.part_number} 上传失败: {e}")

        # 初始进度
        await update_progress()

        # 使用信号量控制并发
        semaphore = asyncio.Semaphore(self.concurrency)

        async def upload_with_semaphore(part: PartInfo):
            async with semaphore:
                await upload_part(part)

        # 并发上传
        tasks = [upload_with_semaphore(part) for part in parts]
        await asyncio.gather(*tasks)

    async def _complete_upload(self, file_id: str, user_id: Optional[str] = None) -> dict:
        """完成上传"""
        payload = {"file_id": file_id}
        if user_id:
            payload["user_id"] = user_id
        return await self._request(
            "POST",
            "/api/community/files/upload/complete",
            json=payload,
        )

    async def abort_upload(self, file_id: str) -> bool:
        """
        取消上传

        Args:
            file_id: 文件 ID

        Returns:
            是否取消成功
        """
        try:
            await self._request(
                "POST",
                "/api/community/files/upload/abort",
                json={"file_id": file_id},
            )
            return True
        except UploadError:
            return False

    def cancel(self):
        """取消当前上传"""
        self._cancelled = True

    # ==================== 文件管理 ====================

    async def get_file_info(self, file_id: str) -> FileInfo:
        """
        获取文件信息

        Args:
            file_id: 文件 ID

        Returns:
            文件信息
        """
        data = await self._request("GET", f"/api/community/files/info/{file_id}")
        return FileInfo.from_dict(data)

    # 批量查询每批最大数量
    BATCH_GET_FILES_LIMIT = 100

    async def batch_get_files(
        self,
        file_ids: List[str],
        fields: Optional[List[Union[FileField, str]]] = None,
    ) -> BatchGetFilesResult:
        """
        批量获取文件信息

        支持一次查询多个文件，并可指定需要返回的字段以减少网络传输。
        该接口支持 GZip 压缩，大批量查询时可显著减少传输数据量。

        当文件数量超过 100 个时，SDK 会自动分批查询并合并结果。

        Args:
            file_ids: 文件ID列表（无数量限制，SDK 自动分批）
            fields: 需要返回的字段列表，不指定则返回全部字段。
                    可以使用 FileField 枚举或字符串。
                    也可以使用预定义的字段集合：
                    - FileField.basic(): 基础信息
                    - FileField.hls(): HLS 相关
                    - FileField.media(): 媒体信息
                    - FileField.video_playback(): 视频播放常用字段

        Returns:
            BatchGetFilesResult: 包含文件列表、找到数量和未找到的ID列表

        Example:
            ```python
            # 获取全部字段
            result = await sdk.batch_get_files(["file_id_1", "file_id_2"])

            # 只获取视频播放需要的字段
            result = await sdk.batch_get_files(
                file_ids=["file_id_1", "file_id_2"],
                fields=FileField.video_playback()
            )

            # 自定义字段
            result = await sdk.batch_get_files(
                file_ids=["file_id_1", "file_id_2"],
                fields=[FileField.ID, FileField.HLS_URL, FileField.THUMBNAIL_URL]
            )

            # 查询大量文件（自动分批）
            result = await sdk.batch_get_files(file_ids=large_file_id_list)  # 支持超过100个

            # 访问结果
            for file in result.files:
                print(f"{file.id}: {file.hls_url}")

            # 转换为字典便于查找
            files_dict = result.as_dict()
            file1 = files_dict.get("file_id_1")
            ```
        """
        if not file_ids:
            return BatchGetFilesResult(files=[], found=0, not_found=[])

        # 将 FileField 枚举转换为字符串
        field_strs = None
        if fields:
            field_strs = [f.value if isinstance(f, FileField) else f for f in fields]

        # 如果文件数量不超过限制，直接查询
        if len(file_ids) <= self.BATCH_GET_FILES_LIMIT:
            return await self._batch_get_files_single(file_ids, field_strs)

        # 分批查询
        all_files: List[FileInfo] = []
        all_not_found: List[str] = []

        for i in range(0, len(file_ids), self.BATCH_GET_FILES_LIMIT):
            batch_ids = file_ids[i:i + self.BATCH_GET_FILES_LIMIT]
            result = await self._batch_get_files_single(batch_ids, field_strs)
            all_files.extend(result.files)
            all_not_found.extend(result.not_found)

        return BatchGetFilesResult(
            files=all_files,
            found=len(all_files),
            not_found=all_not_found
        )

    async def _batch_get_files_single(
        self,
        file_ids: List[str],
        fields: Optional[List[str]] = None,
    ) -> BatchGetFilesResult:
        """
        单批次获取文件信息（内部方法）

        Args:
            file_ids: 文件ID列表，最多100个
            fields: 需要返回的字段列表（已转换为字符串）

        Returns:
            BatchGetFilesResult
        """
        body: Dict[str, Any] = {"file_ids": file_ids}
        if fields:
            body["fields"] = fields

        data = await self._request(
            "POST",
            "/api/community/files/batch",
            json=body,
            headers={"Accept-Encoding": "gzip"}
        )
        return BatchGetFilesResult.from_dict(data)

    def get_file_url(
        self,
        file_id: str,
        variant_name: Optional[str] = None,
    ) -> str:
        """
        获取文件访问 URL

        返回文件服务的代理 URL，访问时会 302 重定向到真实的 OSS 地址。

        Args:
            file_id: 文件 ID
            variant_name: 文件变体，可选值：
                - None 或 'origin': 原始文件（默认）
                - 'poster': 视频封面图
                - 'hls': HLS 主播放列表
                - 'small': 低分辨率视频（优先360p）
                - 'medium': 中等分辨率视频（优先720p）
                - 'large': 高分辨率视频（优先1080p）

        Returns:
            文件访问 URL

        Example:
            ```python
            # 获取原始文件 URL
            url = sdk.get_file_url(file_id)

            # 获取视频封面
            poster_url = sdk.get_file_url(file_id, variant_name='poster')

            # 获取低分辨率视频（用于预览）
            small_url = sdk.get_file_url(file_id, variant_name='small')
            ```
        """
        url = f"{self.base_url}/api/community/files/{file_id}"
        if variant_name:
            url = f"{url}?variant={variant_name}"
        return url

    async def wait_for_file_ready(
        self,
        file_id: str,
        timeout: float = 600.0,
        initial_interval: float = 2.0,
        max_interval: float = 30.0,
        backoff_factor: float = 1.5,
        on_progress: Optional[Callable[[FileInfo], None]] = None,
    ) -> FileInfo:
        """
        等待文件处理完成（元数据提取和 HLS 转码）

        使用指数退避策略轮询文件状态，直到处理完成、失败或超时。

        Args:
            file_id: 文件 ID
            timeout: 超时时间（秒），默认 600 秒（10分钟）
            initial_interval: 初始轮询间隔（秒），默认 2 秒
            max_interval: 最大轮询间隔（秒），默认 30 秒
            backoff_factor: 退避因子，默认 1.5
            on_progress: 进度回调函数

        Returns:
            处理完成的文件信息

        Raises:
            TimeoutError: 等待超时
            UploadError: 处理失败

        Example:
            ```python
            # 上传后等待处理完成
            result = await sdk.upload(video_file)
            file_info = await sdk.wait_for_file_ready(
                result.file.id,
                on_progress=lambda info: print(f"状态: metadata={info.task_status}")
            )

            # 获取处理后的视频变体
            small_url = sdk.get_file_url(file_info.id, variant_name='small')
            ```
        """
        import time
        start_time = time.time()
        interval = initial_interval
        attempt = 0

        while True:
            attempt += 1
            elapsed = time.time() - start_time

            # 检查超时
            if elapsed >= timeout:
                raise TimeoutError(f"等待文件处理超时（{timeout}秒）: file_id={file_id}")

            # 获取文件信息
            try:
                file_info = await self.get_file_info(file_id)
            except UploadError as e:
                if e.code == 404:
                    raise ValueError(f"文件不存在: {file_id}")
                raise

            # 回调
            if on_progress:
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(file_info)
                else:
                    on_progress(file_info)

            # 获取任务状态
            task_status = file_info.extra_metadata.get('tasks', {}) if file_info.extra_metadata else {}
            metadata_task = task_status.get('metadata_extract', {})
            metadata_status = metadata_task.get('status') if isinstance(metadata_task, dict) else None

            # 对于视频，还需要检查 HLS 状态
            hls_status = file_info.hls_status

            self._log(
                f"[尝试 {attempt}] 等待文件处理: file_id={file_id}, "
                f"metadata_extract={metadata_status}, hls_transcode={hls_status}, "
                f"已等待 {elapsed:.1f}s"
            )

            # 检查是否处理失败
            if metadata_status == 'failed':
                raise UploadError(f"文件元数据提取失败: file_id={file_id}")
            if hls_status == 'failed':
                raise UploadError(f"HLS 转码失败: file_id={file_id}")

            # 检查是否处理完成
            # 对于视频：需要 metadata 完成 + HLS 完成/部分完成
            # 对于非视频：只需要 metadata 完成（或无需处理）
            is_video = file_info.category == 'video'

            if is_video:
                if metadata_status == 'completed' and hls_status in ('completed', 'partial'):
                    self._log(f"文件处理完成: file_id={file_id}, 总等待时间 {elapsed:.1f}s")
                    return file_info
            else:
                # 非视频文件：metadata 完成或已有媒体信息
                media_info = file_info.extra_metadata.get('media_info') if file_info.extra_metadata else None
                if metadata_status == 'completed' or media_info:
                    self._log(f"文件处理完成: file_id={file_id}, 总等待时间 {elapsed:.1f}s")
                    return file_info
                # 非媒体文件（如文档）可能不需要处理
                if file_info.category not in ('video', 'image', 'audio'):
                    self._log(f"非媒体文件，无需等待处理: file_id={file_id}")
                    return file_info

            # 等待后重试（指数退避）
            self._log(f"文件处理中，{interval:.1f}s 后重试...")
            await asyncio.sleep(interval)

            # 增加间隔（指数退避）
            interval = min(interval * backoff_factor, max_interval)

    async def get_file_by_url(self, url: str) -> FileInfo:
        """
        通过 URL 获取文件信息

        自动从各种 URL 格式中提取信息：
        - 文件服务代理 URL: /api/community/files/{file_id} -> 使用 file_id 查询
        - OSS URL: https://bucket.oss-accelerate.aliyuncs.com/community/videos/xxx.mp4 -> 使用 file_key 查询
        - ImageKit URL: https://ik.imagekit.io/tapnow/community/videos/xxx.mp4 -> 使用 file_key 查询
        - 直接 file_key: community/videos/xxx.mp4 -> 使用 file_key 查询

        Args:
            url: 文件 URL 或 file_key

        Returns:
            文件信息
        """
        # 优先尝试提取 file_id（文件服务代理 URL）
        file_id = self.extract_file_id(url)
        if file_id:
            return await self.get_file_info(file_id)

        # 尝试提取 file_key（OSS/ImageKit URL）
        file_key = self.extract_file_key(url)
        if not file_key:
            raise ValueError("无效的 URL 格式，无法提取 file_key 或 file_id")

        data = await self._request("GET", "/api/community/files/by-key", params={"file_key": file_key})
        return FileInfo.from_dict(data)

    @staticmethod
    def extract_file_key(url: str) -> Optional[str]:
        """
        从 URL 中提取 file_key

        支持：
        - OSS URL: https://bucket.oss-xxx.aliyuncs.com/path/to/file.mp4
        - ImageKit URL: https://ik.imagekit.io/tapnow/path/to/file.mp4
        - 直接 file_key: path/to/file.mp4

        注意：文件服务代理 URL（/api/community/files/{file_id}）返回 None，
        应使用 extract_file_id 提取 file_id 后调用 get_file_info

        Args:
            url: 文件 URL 或 file_key

        Returns:
            提取的 file_key，如果无效则返回 None
        """
        if not url:
            return None

        if "://" not in url:
            return url.lstrip("/")

        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            hostname = parsed.hostname or ""
            pathname = parsed.path.lstrip("/")

            # 文件服务代理 URL，不是 file_key
            if pathname.startswith("api/community/files/"):
                return None

            if "aliyuncs.com" in hostname:
                return pathname

            if "imagekit.io" in hostname:
                parts = pathname.split("/")
                if len(parts) > 1:
                    return "/".join(parts[1:])
                return pathname

            return pathname
        except Exception:
            return None

    @staticmethod
    def extract_file_id(url: str) -> Optional[str]:
        """
        从文件服务代理 URL 中提取 file_id

        支持：
        - /api/community/files/{file_id}
        - http://host/api/community/files/{file_id}
        - http://host/api/community/files/{file_id}?variant=small

        Args:
            url: 文件服务代理 URL

        Returns:
            提取的 file_id，如果无效则返回 None
        """
        if not url:
            return None

        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            pathname = parsed.path.lstrip("/")

            # 匹配 api/community/files/{file_id} 格式
            if pathname.startswith("api/community/files/"):
                # 去掉前缀，获取 file_id（可能带有子路径如 /info）
                remainder = pathname[len("api/community/files/"):]
                # 取第一段作为 file_id
                file_id = remainder.split("/")[0]
                if file_id:
                    return file_id

            return None
        except Exception:
            return None

    async def list_files(
        self, params: Optional[ListFilesParams] = None
    ) -> tuple[List[FileInfo], int]:
        """
        获取文件列表

        Args:
            params: 查询参数

        Returns:
            (文件列表, 总数)
        """
        params = params or ListFilesParams()
        query = {
            "page": params.page,
            "page_size": params.page_size,
        }
        if params.category:
            query["category"] = params.category
        if params.status:
            query["status"] = params.status

        data = await self._request("GET", "/api/community/files", params=query)

        files = [FileInfo.from_dict(f) for f in data.get("list", [])]
        total = data.get("pagination", {}).get("total", 0)

        return files, total

    async def delete_file(self, file_id: str) -> bool:
        """
        删除文件

        Args:
            file_id: 文件 ID

        Returns:
            是否删除成功
        """
        try:
            await self._request("DELETE", f"/api/community/files/{file_id}")
            return True
        except UploadError:
            return False

    # ==================== HLS 方法 ====================

    async def get_hls_info(self, url: str) -> HLSInfo:
        """
        获取视频的 HLS 播放信息

        Args:
            url: 视频 URL（OSS URL、ImageKit URL 或 file_key）

        Returns:
            HLS 信息，包含 master_url 和各变体详情

        Example:
            ```python
            info = await sdk.get_hls_info('https://ik.imagekit.io/tapnow/community/videos/xxx.mp4')
            if info.hls_available:
                print(f"HLS 播放地址: {info.master_url}")
            ```
        """
        file_key = self.extract_file_key(url)
        if not file_key:
            raise ValueError("无效的 URL 格式，无法提取 file_key")

        data = await self._request("GET", "/api/community/files/hls/by-key", params={"file_key": file_key})
        return HLSInfo.from_dict(data)

    async def get_hls_info_by_id(self, file_id: str) -> HLSInfo:
        """
        通过文件 ID 获取 HLS 信息

        Args:
            file_id: 文件 ID

        Returns:
            HLS 信息
        """
        data = await self._request("GET", f"/api/community/files/hls/{file_id}")
        return HLSInfo.from_dict(data)

    async def trigger_hls_transcode(self, file_id: str) -> Dict[str, Any]:
        """
        手动触发/重试 HLS 转码

        注意：视频上传完成后会自动触发 HLS 转码，此方法主要用于：
        1. 转码失败后手动重试
        2. 需要重新生成 HLS 流的场景

        Args:
            file_id: 文件 ID

        Returns:
            转码任务信息
        """
        return await self._request("POST", f"/api/community/files/hls/{file_id}/transcode")

    async def wait_for_hls(
        self,
        url: str,
        interval: float = 3.0,
        timeout: float = 600.0,
        on_progress: Optional[Callable[[HLSInfo], None]] = None,
    ) -> HLSInfo:
        """
        等待 HLS 转码完成

        轮询 HLS 状态，直到转码完成、失败或超时。

        Args:
            url: 视频 URL（OSS URL、ImageKit URL 或 file_key）
            interval: 轮询间隔（秒），默认 3 秒
            timeout: 超时时间（秒），默认 600 秒（10分钟）
            on_progress: 进度回调

        Returns:
            最终的 HLS 信息

        Raises:
            TimeoutError: 转码超时
            UploadError: 转码失败

        Example:
            ```python
            result = await sdk.upload(video_file)
            hls_info = await sdk.wait_for_hls(
                result.file.imagekit_url,
                on_progress=lambda info: print(f"状态: {info.hls_status}")
            )
            ```
        """
        import time
        start_time = time.time()

        while True:
            info = await self.get_hls_info(url)

            if on_progress:
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(info)
                else:
                    on_progress(info)

            # 检查是否完成
            if info.hls_status in ("completed", "partial"):
                self._log(f"HLS 转码完成: {info.hls_status}")
                return info

            if info.hls_status == "failed":
                raise UploadError("HLS 转码失败")

            # 检查超时
            if time.time() - start_time > timeout:
                raise TimeoutError("HLS 转码超时")

            # 等待后继续轮询
            self._log(f"HLS 状态: {info.hls_status}，等待 {interval}s...")
            await asyncio.sleep(interval)
