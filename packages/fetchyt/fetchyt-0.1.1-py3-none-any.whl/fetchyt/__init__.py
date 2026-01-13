"""FetchYT - Download MP3s from YouTube playlists.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

__version__ = "0.1.0"
__author__ = "Krishnakanth Allika"
__copyright__ = "Copyright (c) 2024-2026 Krishnakanth Allika"
__description__ = (
    "Download MP3s from YouTube playlists with FastAPI backend and web interface"
)

from .downloader import YouTubeDownloader
from .models import DownloadRequest, DownloadResponse, DownloadStatus

__all__ = [
    "YouTubeDownloader",
    "DownloadRequest",
    "DownloadResponse",
    "DownloadStatus",
]
