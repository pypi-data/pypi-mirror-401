"""
类型定义
"""
from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Awaitable, Union, List, Dict
from enum import Enum


# 进度回调类型
ProgressCallback = Callable[[float], None]
AsyncProgressCallback = Callable[[float], Awaitable[None]]


class FileCategory(str, Enum):
    """文件分类"""
    GENERAL = "general"
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"
    DOCUMENT = "document"
    AVATAR = "avatar"
    COVER = "cover"


class FileStatus(str, Enum):
    """文件状态"""
    PENDING = "pending"
    UPLOADING = "uploading"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class HLSVariantStatus(str, Enum):
    """HLS 变体状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class HLSStatus(str, Enum):
    """HLS 整体状态"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass
class HLSVariant:
    """HLS 变体信息"""
    name: str  # 变体名称，如 '360p', '720p'
    resolution: str  # 分辨率，如 '1280x720'
    bandwidth: int  # 带宽 (bps)
    status: str  # 变体状态
    playlist_key: Optional[str] = None  # OSS 中的播放列表 key
    segment_count: Optional[int] = None  # 分片数量
    url: Optional[str] = None  # 变体播放列表 URL（完整 URL）
    mp4_key: Optional[str] = None  # OSS 中的 MP4 文件 key
    mp4_url: Optional[str] = None  # MP4 文件 URL（完整 URL）
    error: Optional[str] = None  # 错误信息

    @classmethod
    def from_dict(cls, data: dict) -> "HLSVariant":
        """从字典创建"""
        return cls(
            name=data.get("name", ""),
            resolution=data.get("resolution", ""),
            bandwidth=data.get("bandwidth", 0),
            status=data.get("status", "pending"),
            playlist_key=data.get("playlist_key"),
            segment_count=data.get("segment_count"),
            url=data.get("url"),
            mp4_key=data.get("mp4_key"),
            mp4_url=data.get("mp4_url"),
            error=data.get("error"),
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            "name": self.name,
            "resolution": self.resolution,
            "bandwidth": self.bandwidth,
            "status": self.status,
            "playlist_key": self.playlist_key,
            "segment_count": self.segment_count,
            "url": self.url,
            "error": self.error,
        }
        if self.mp4_key:
            result["mp4_key"] = self.mp4_key
        if self.mp4_url:
            result["mp4_url"] = self.mp4_url
        return result


@dataclass
class HLSInfo:
    """HLS 播放信息"""
    file_id: str  # 文件 ID
    hls_status: Optional[str]  # HLS 整体状态
    hls_available: bool  # HLS 是否可用
    variants: List[HLSVariant]  # 变体列表
    original_url: str  # 原始视频 URL（降级使用）
    master_url: Optional[str] = None  # 主播放列表 URL

    @classmethod
    def from_dict(cls, data: dict) -> "HLSInfo":
        """从字典创建"""
        variants_data = data.get("variants", [])
        variants = [HLSVariant.from_dict(v) for v in variants_data]
        return cls(
            file_id=data.get("file_id", ""),
            hls_status=data.get("hls_status"),
            hls_available=data.get("hls_available", False),
            variants=variants,
            original_url=data.get("original_url", ""),
            master_url=data.get("master_url"),
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "file_id": self.file_id,
            "hls_status": self.hls_status,
            "hls_available": self.hls_available,
            "variants": [v.to_dict() for v in self.variants],
            "original_url": self.original_url,
            "master_url": self.master_url,
        }


@dataclass
class FileInfo:
    """文件信息"""
    id: str
    url: Optional[str] = None  # 服务代理 URL（推荐使用）
    file_key: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    file_ext: Optional[str] = None
    file_hash: Optional[str] = None  # SHA-256 哈希
    bucket: Optional[str] = None
    region: Optional[str] = None
    oss_url: Optional[str] = None
    imagekit_url: Optional[str] = None
    cdn_url: Optional[str] = None
    category: str = "general"
    user_id: Optional[str] = None
    org_id: Optional[str] = None
    status: str = "pending"
    related_type: Optional[str] = None
    related_id: Optional[str] = None
    extra_metadata: dict = field(default_factory=dict)
    # HLS 相关字段
    hls_status: Optional[str] = None  # HLS 转码状态
    hls_variants: Optional[List[HLSVariant]] = None  # HLS 变体信息
    hls_url: Optional[str] = None  # HLS 主播放列表 URL
    hls_master_key: Optional[str] = None  # HLS 主播放列表 OSS Key
    # 媒体信息（精简返回时提供）
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[float] = None
    thumbnail_url: Optional[str] = None
    thumbnail_file_id: Optional[str] = None  # 封面图文件 ID
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    confirmed_at: Optional[str] = None
    deleted_at: Optional[str] = None
    deduplicated: Optional[bool] = None  # 是否命中去重（仅上传结果中存在）

    @classmethod
    def from_dict(cls, data: dict) -> "FileInfo":
        """从字典创建 FileInfo 对象"""
        # 处理 HLS 变体
        # 优先使用 variants 字段（包含完整 URL），否则使用 hls_variants（原始数据）
        variants_data = data.get("variants") or data.get("hls_variants")
        hls_variants = None
        if variants_data:
            hls_variants = [HLSVariant.from_dict(v) for v in variants_data]

        # 从 media_info 中提取媒体信息（width, height, duration）
        # 优先使用根级别的值，如果没有则从 media_info 中获取
        media_info = data.get("media_info") or {}
        width = data.get("width") if data.get("width") is not None else media_info.get("width")
        height = data.get("height") if data.get("height") is not None else media_info.get("height")
        duration = data.get("duration") if data.get("duration") is not None else media_info.get("duration")

        return cls(
            id=data.get("id", ""),
            url=data.get("url"),
            file_key=data.get("file_key"),
            file_size=data.get("file_size"),
            file_type=data.get("file_type"),
            file_ext=data.get("file_ext"),
            file_hash=data.get("file_hash"),
            bucket=data.get("bucket"),
            region=data.get("region"),
            oss_url=data.get("oss_url"),
            imagekit_url=data.get("imagekit_url"),
            cdn_url=data.get("cdn_url"),
            category=data.get("category", "general"),
            user_id=data.get("user_id"),
            org_id=data.get("org_id"),
            status=data.get("status", "pending"),
            related_type=data.get("related_type"),
            related_id=data.get("related_id"),
            extra_metadata=data.get("extra_metadata", {}),
            hls_status=data.get("hls_status"),
            hls_variants=hls_variants,
            hls_url=data.get("hls_url"),
            hls_master_key=data.get("hls_master_key"),
            width=width,
            height=height,
            duration=duration,
            thumbnail_url=data.get("thumbnail_url"),
            thumbnail_file_id=data.get("thumbnail_file_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            confirmed_at=data.get("confirmed_at"),
            deleted_at=data.get("deleted_at"),
            deduplicated=data.get("deduplicated"),
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        result = {
            "id": self.id,
            "url": self.url,
            "file_key": self.file_key,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "file_ext": self.file_ext,
            "file_hash": self.file_hash,
            "bucket": self.bucket,
            "region": self.region,
            "oss_url": self.oss_url,
            "imagekit_url": self.imagekit_url,
            "cdn_url": self.cdn_url,
            "category": self.category,
            "user_id": self.user_id,
            "org_id": self.org_id,
            "status": self.status,
            "related_type": self.related_type,
            "related_id": self.related_id,
            "extra_metadata": self.extra_metadata,
            "hls_status": self.hls_status,
            "hls_variants": [v.to_dict() for v in self.hls_variants] if self.hls_variants else None,
            "hls_url": self.hls_url,
            "hls_master_key": self.hls_master_key,
            "width": self.width,
            "height": self.height,
            "duration": self.duration,
            "thumbnail_url": self.thumbnail_url,
            "thumbnail_file_id": self.thumbnail_file_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "confirmed_at": self.confirmed_at,
            "deleted_at": self.deleted_at,
        }
        if self.deduplicated is not None:
            result["deduplicated"] = self.deduplicated
        return result


@dataclass
class UploadResult:
    """上传结果"""
    file: FileInfo
    deduplicated: bool = False  # 是否命中去重（秒传）

    @classmethod
    def from_dict(cls, data: dict, deduplicated: bool = False) -> "UploadResult":
        """从字典创建"""
        return cls(
            file=FileInfo.from_dict(data),
            deduplicated=deduplicated,
        )


@dataclass
class UploadOptions:
    """上传选项"""
    category: str = "general"
    content_type: Optional[str] = None
    part_size: Optional[int] = None
    metadata: Optional[dict] = None
    on_progress: Optional[Union[ProgressCallback, AsyncProgressCallback]] = None
    on_hash_progress: Optional[Union[ProgressCallback, AsyncProgressCallback]] = None  # SHA-256 计算进度
    # API Key 认证时可指定用户信息（覆盖客户端级别的设置）
    user_id: Optional[str] = None
    org_id: Optional[str] = None


@dataclass
class ListFilesParams:
    """文件列表查询参数"""
    category: Optional[str] = None
    status: Optional[str] = None
    page: int = 1
    page_size: int = 20


class FileField(str, Enum):
    """
    文件信息可选字段

    用于 batch_get_files 方法指定需要返回的字段，减少网络传输。
    """
    # 基础信息
    ID = "id"
    URL = "url"
    FILE_KEY = "file_key"
    FILE_SIZE = "file_size"
    FILE_TYPE = "file_type"
    CATEGORY = "category"
    STATUS = "status"

    # HLS 相关
    HLS_STATUS = "hls_status"
    HLS_URL = "hls_url"
    HLS_VARIANTS = "hls_variants"
    HLS_MASTER_KEY = "hls_master_key"

    # 媒体信息
    THUMBNAIL_URL = "thumbnail_url"
    THUMBNAIL_FILE_ID = "thumbnail_file_id"
    MEDIA_INFO = "media_info"
    WIDTH = "width"
    HEIGHT = "height"
    DURATION = "duration"

    # 时间信息
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

    @classmethod
    def basic(cls) -> List["FileField"]:
        """基础信息字段集合"""
        return [cls.ID, cls.URL, cls.FILE_SIZE, cls.FILE_TYPE, cls.CATEGORY, cls.STATUS]

    @classmethod
    def hls(cls) -> List["FileField"]:
        """HLS 相关字段集合"""
        return [cls.HLS_STATUS, cls.HLS_URL, cls.HLS_VARIANTS, cls.HLS_MASTER_KEY]

    @classmethod
    def media(cls) -> List["FileField"]:
        """媒体信息字段集合"""
        return [cls.THUMBNAIL_URL, cls.THUMBNAIL_FILE_ID, cls.WIDTH, cls.HEIGHT, cls.DURATION]

    @classmethod
    def video_playback(cls) -> List["FileField"]:
        """视频播放所需的常用字段集合"""
        return [
            cls.ID, cls.URL, cls.STATUS,
            cls.HLS_STATUS, cls.HLS_URL, cls.HLS_VARIANTS,
            cls.THUMBNAIL_URL, cls.WIDTH, cls.HEIGHT, cls.DURATION
        ]


@dataclass
class BatchGetFilesResult:
    """批量获取文件信息结果"""
    files: List[FileInfo]  # 文件信息列表
    found: int  # 找到的文件数量
    not_found: List[str]  # 未找到的文件ID列表

    @classmethod
    def from_dict(cls, data: dict) -> "BatchGetFilesResult":
        """从字典创建"""
        files_data = data.get("files", [])
        files = [FileInfo.from_dict(f) for f in files_data]
        return cls(
            files=files,
            found=data.get("found", len(files)),
            not_found=data.get("not_found", []),
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "files": [f.to_dict() for f in self.files],
            "found": self.found,
            "not_found": self.not_found,
        }

    def get_file(self, file_id: str) -> Optional[FileInfo]:
        """通过文件ID获取文件信息"""
        for f in self.files:
            if f.id == file_id:
                return f
        return None

    def as_dict(self) -> Dict[str, FileInfo]:
        """将文件列表转换为字典，key为file_id"""
        return {f.id: f for f in self.files}


@dataclass
class PartInfo:
    """分片信息"""
    part_number: int
    start: int
    end: int
    size: int
    upload_url: Optional[str] = None
    uploaded: bool = False
    etag: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PartInfo":
        """从字典创建"""
        return cls(
            part_number=data.get("part_number", 0),
            start=data.get("start", 0),
            end=data.get("end", 0),
            size=data.get("size", 0),
            upload_url=data.get("upload_url"),
            uploaded=data.get("uploaded", False),
            etag=data.get("etag"),
        )
