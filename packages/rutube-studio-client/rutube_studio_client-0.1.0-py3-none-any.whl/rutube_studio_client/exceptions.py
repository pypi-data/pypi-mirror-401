class RutubeError(Exception):
    """Base exception"""

class AuthError(RutubeError):
    """Login failed"""

class UploadError(RutubeError):
    """Video upload failed"""
