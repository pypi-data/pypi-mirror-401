"""Data models for FetchYT.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class DownloadStatus(str, Enum):
    """Download status enum."""

    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"


class DownloadRequest(BaseModel):
    """Request model for downloading."""

    url: str = Field(..., description="YouTube playlist or video URL")
    format: str = Field(default="mp3", description="Output format (mp3, m4a, etc.)")
    quality: str = Field(default="192", description="Audio quality in kbps")


class VideoInfo(BaseModel):
    """Video information model."""

    id: str
    title: str
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None


class DownloadProgress(BaseModel):
    """Download progress model."""

    video_id: str
    status: DownloadStatus
    progress: float = 0.0  # 0-100
    filename: Optional[str] = None
    error: Optional[str] = None


class DownloadResponse(BaseModel):
    """Response model for download operations."""

    task_id: str
    status: DownloadStatus
    message: str
    videos: List[VideoInfo] = []


class DownloadStatusResponse(BaseModel):
    """Response model for download status check."""

    task_id: str
    status: DownloadStatus
    progress: List[DownloadProgress] = []
    completed: int = 0
    total: int = 0
