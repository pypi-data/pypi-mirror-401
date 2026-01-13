from typing import Optional, List
from pydantic import BaseModel, Field

class VideoStats(BaseModel):
    views: int
    likes: int = 0
    comments: int = 0

class Video(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    duration: Optional[int] = 0
    cover_url: Optional[str] = Field(None, alias="thumbnail_url")
    is_hidden: bool = False
    stats: Optional[VideoStats] = None

class UploadSession(BaseModel):
    upload_url: str
    video_id: str
    # Поля могут отличаться в зависимости от реального ответа Rutube
