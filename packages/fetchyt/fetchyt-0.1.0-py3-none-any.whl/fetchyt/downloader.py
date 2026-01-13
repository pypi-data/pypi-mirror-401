"""YouTube downloader core functionality.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

import asyncio
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Callable
import yt_dlp

from .config import settings
from .models import (
    DownloadStatus,
    DownloadProgress,
    VideoInfo,
)


class YouTubeDownloader:
    """YouTube downloader with playlist support."""

    def __init__(self, download_dir: Optional[Path] = None):
        """Initialize downloader.

        Args:
            download_dir: Directory to save downloads. Uses settings default if not provided.
        """
        self.download_dir = download_dir or settings.ensure_download_dir()
        self.active_downloads: Dict[str, Dict] = {}
        self._progress_callbacks: Dict[str, Callable] = {}

    @staticmethod
    def extract_cookies_from_browser(
        browser: str = "chrome", output_file: Optional[Path] = None
    ) -> Path:
        """Extract cookies from browser and save to file using yt-dlp.

        Args:
            browser: Browser name ('chrome', 'firefox', 'edge', 'safari', etc.)
            output_file: Path to save cookies. Defaults to 'cookies.txt' in current directory.

        Returns:
            Path to the cookies file

        Raises:
            Exception: If cookie extraction fails
        """
        import subprocess

        if output_file is None:
            output_file = Path("cookies.txt")

        try:
            # Use yt-dlp's built-in cookie extraction
            result = subprocess.run(
                [
                    "yt-dlp",
                    "--cookies-from-browser",
                    browser,
                    "--cookies",
                    str(output_file),
                    "--no-warnings",
                    "https://www.youtube.com",  # Dummy URL
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                raise Exception(
                    result.stderr or f"Failed to extract cookies from {browser}"
                )

            if not output_file.exists():
                raise Exception(f"Cookie file was not created at {output_file}")

            return output_file

        except subprocess.TimeoutExpired:
            raise Exception(
                f"Cookie extraction timed out. Make sure {browser} is running and you're logged into YouTube."
            )
        except FileNotFoundError:
            raise Exception(
                "yt-dlp command not found. Please ensure yt-dlp is installed and in PATH:\n"
                "  pip install --upgrade yt-dlp"
            )

    def _get_ydl_opts(self, format: str = "mp3", quality: str = "192") -> dict:
        """Get yt-dlp options.

        Args:
            format: Audio format (mp3, m4a, etc.)
            quality: Audio quality in kbps

        Returns:
            Dictionary of yt-dlp options
        """
        return {
            "format": settings.YOUTUBE_DL_FORMAT,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": format,
                    "preferredquality": quality,
                }
            ],
            "outtmpl": str(self.download_dir / "%(title)s.%(ext)s"),
            "quiet": False,
            "no_warnings": False,
            "ignoreerrors": True,  # Continue on download errors
        }

    async def extract_info(
        self, url: str, browser: Optional[str] = None
    ) -> List[VideoInfo]:
        """Extract video/playlist information without downloading.

        Args:
            url: YouTube video or playlist URL
            browser: Browser to extract cookies from ('chrome', 'firefox', etc.).
                    If provided, will attempt to extract cookies from this browser.

        Returns:
            List of VideoInfo objects

        Raises:
            Exception: If extraction fails due to authentication or other errors
        """
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": "in_playlist",
            "socket_timeout": 30,
            # Add headers to appear more like a real browser
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            # Retry on network errors
            "retries": 5,
        }

        # Add cookies file if configured
        if settings.COOKIES_FILE and settings.COOKIES_FILE.exists():
            ydl_opts["cookiefile"] = str(settings.COOKIES_FILE)
        # Or use browser cookies if specified
        elif browser:
            ydl_opts["cookies_from_browser"] = (browser,)

        def _extract():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

                    # Handle single video
                    if "entries" not in info:
                        return [
                            VideoInfo(
                                id=info.get("id", "unknown"),
                                title=info.get("title", "Unknown"),
                                duration=info.get("duration"),
                                thumbnail=info.get("thumbnail"),
                                uploader=info.get("uploader"),
                            )
                        ]

                    # Handle playlist
                    videos = []
                    for entry in info["entries"]:
                        if entry:  # Some entries might be None
                            videos.append(
                                VideoInfo(
                                    id=entry.get("id", "unknown"),
                                    title=entry.get("title", "Unknown"),
                                    duration=entry.get("duration"),
                                    thumbnail=entry.get("thumbnail"),
                                    uploader=entry.get("uploader"),
                                )
                            )
                    return videos
            except Exception as e:
                # Handle YouTube bot detection and authentication errors
                error_msg = str(e)
                if "Sign in to confirm" in error_msg or "bot" in error_msg.lower():
                    raise Exception(
                        "❌ YouTube Bot Detection Block\n\n"
                        "YouTube is blocking automated requests. Try one of these solutions:\n\n"
                        "Option 1: Extract cookies from Chrome (easiest)\n"
                        "  Make sure Chrome is open and logged into YouTube, then:\n"
                        "  fetchyt cookies --browser chrome\n"
                        "  $env:COOKIES_FILE = './cookies.txt'  # PowerShell\n"
                        '  fetchyt info "<URL>"\n\n'
                        "Option 2: Try Firefox instead\n"
                        "  fetchyt cookies --browser firefox\n"
                        "  $env:COOKIES_FILE = './cookies.txt'\n"
                        '  fetchyt info "<URL>"\n\n'
                        "Option 3: Wait and retry\n"
                        "  YouTube may unblock you after 10-30 minutes. Try again later.\n\n"
                        "Option 4: Use a VPN\n"
                        "  Switch to a different network/VPN and try again.\n\n"
                        "For detailed help: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies"
                    )
                raise

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _extract)

    def _progress_hook(self, task_id: str, d: dict):
        """Progress hook for yt-dlp.

        Args:
            task_id: Task identifier
            d: Progress dictionary from yt-dlp
        """
        if task_id not in self.active_downloads:
            return

        status = d.get("status")
        video_id = d.get("info_dict", {}).get("id", "unknown")

        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            progress = (downloaded / total * 100) if total > 0 else 0

            progress_obj = DownloadProgress(
                video_id=video_id,
                status=DownloadStatus.DOWNLOADING,
                progress=progress,
                filename=d.get("filename"),
            )
        elif status == "finished":
            progress_obj = DownloadProgress(
                video_id=video_id,
                status=DownloadStatus.COMPLETED,
                progress=100.0,
                filename=d.get("filename"),
            )
        else:
            progress_obj = DownloadProgress(
                video_id=video_id,
                status=DownloadStatus.PENDING,
                progress=0.0,
            )

        # Update progress in active downloads
        if "progress" not in self.active_downloads[task_id]:
            self.active_downloads[task_id]["progress"] = {}

        self.active_downloads[task_id]["progress"][video_id] = progress_obj

        # Call progress callback if registered
        if task_id in self._progress_callbacks:
            self._progress_callbacks[task_id](progress_obj)

    async def download(
        self,
        url: str,
        format: str = "mp3",
        quality: str = "192",
        task_id: Optional[str] = None,
        progress_callback: Optional[Callable] = None,
    ) -> str:
        """Download video or playlist.

        Args:
            url: YouTube video or playlist URL
            format: Audio format (mp3, m4a, etc.)
            quality: Audio quality in kbps
            task_id: Optional task ID for tracking
            progress_callback: Optional callback for progress updates

        Returns:
            Task ID for tracking download progress
        """
        if task_id is None:
            task_id = str(uuid.uuid4())

        # Register progress callback
        if progress_callback:
            self._progress_callbacks[task_id] = progress_callback

        # Initialize task tracking
        self.active_downloads[task_id] = {
            "status": DownloadStatus.DOWNLOADING,
            "url": url,
            "progress": {},
        }

        ydl_opts = self._get_ydl_opts(format, quality)
        ydl_opts["progress_hooks"] = [lambda d: self._progress_hook(task_id, d)]

        def _download():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                self.active_downloads[task_id]["status"] = DownloadStatus.COMPLETED
            except Exception as e:
                self.active_downloads[task_id]["status"] = DownloadStatus.FAILED
                self.active_downloads[task_id]["error"] = str(e)

        # Run download in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _download)

        # Clean up callback
        if task_id in self._progress_callbacks:
            del self._progress_callbacks[task_id]

        return task_id

    def get_download_status(self, task_id: str) -> Optional[Dict]:
        """Get status of a download task.

        Args:
            task_id: Task identifier

        Returns:
            Dictionary with download status or None if not found
        """
        return self.active_downloads.get(task_id)

    def cleanup_task(self, task_id: str):
        """Remove task from active downloads.

        Args:
            task_id: Task identifier
        """
        if task_id in self.active_downloads:
            del self.active_downloads[task_id]
        if task_id in self._progress_callbacks:
            del self._progress_callbacks[task_id]
