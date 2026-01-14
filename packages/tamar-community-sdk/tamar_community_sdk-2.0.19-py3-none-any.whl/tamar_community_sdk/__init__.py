"""
Tamar Community SDK for Python

支持文件上传、HLS视频流、文件管理的异步客户端
"""
from .sdk import TamarCommunitySDK
from .types import (
    FileInfo,
    UploadResult,
    UploadOptions,
    ListFilesParams,
    ProgressCallback,
    HLSInfo,
    HLSVariant,
    HLSStatus,
    HLSVariantStatus,
    FileField,
    BatchGetFilesResult,
)
from .exceptions import (
    UploadError,
    AuthError,
    NetworkError,
    AbortError,
)

__version__ = "2.1.0"
__all__ = [
    "TamarCommunitySDK",
    "FileInfo",
    "UploadResult",
    "UploadOptions",
    "ListFilesParams",
    "ProgressCallback",
    "HLSInfo",
    "HLSVariant",
    "HLSStatus",
    "HLSVariantStatus",
    "FileField",
    "BatchGetFilesResult",
    "UploadError",
    "AuthError",
    "NetworkError",
    "AbortError",
]
