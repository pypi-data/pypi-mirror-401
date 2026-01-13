# rutube/__init__.py

from .client import RutubeClient
from .models import Video, VideoStats, UploadSession
from .exceptions import RutubeError, AuthError, UploadError

__version__ = "0.1.0"

__all__ = [
    "RutubeClient",
    "Video",
    "VideoStats",
    "UploadSession",
    "RutubeError",
    "AuthError",
    "UploadError",
]
