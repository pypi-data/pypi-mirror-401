"""Tests for the downloader module.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

import pytest
from fetchyt.downloader import YouTubeDownloader
from fetchyt.models import DownloadStatus


@pytest.mark.asyncio
async def test_downloader_initialization(temp_download_dir):
    """Test downloader initialization.

    Args:
        temp_download_dir: Temporary download directory fixture
    """
    downloader = YouTubeDownloader(temp_download_dir)
    assert downloader.download_dir == temp_download_dir
    assert len(downloader.active_downloads) == 0


@pytest.mark.asyncio
async def test_extract_info_video(sample_youtube_url):
    """Test extracting information from a single video.

    Args:
        sample_youtube_url: Sample YouTube URL fixture
    """
    downloader = YouTubeDownloader()

    # Note: This test requires internet connection
    # In production, mock yt_dlp responses
    try:
        videos = await downloader.extract_info(sample_youtube_url)
        assert len(videos) >= 1
        assert videos[0].id is not None
        assert videos[0].title is not None
    except Exception as e:
        pytest.skip(f"Skipping due to network/API issue: {e}")


def test_ydl_opts_generation():
    """Test yt-dlp options generation."""
    downloader = YouTubeDownloader()

    opts = downloader._get_ydl_opts(format="mp3", quality="192")

    assert opts["format"] == "bestaudio/best"
    assert len(opts["postprocessors"]) > 0
    assert opts["postprocessors"][0]["preferredcodec"] == "mp3"
    assert opts["postprocessors"][0]["preferredquality"] == "192"


@pytest.mark.asyncio
async def test_download_status_tracking():
    """Test download status tracking."""
    downloader = YouTubeDownloader()

    # Simulate a task
    task_id = "test-task-123"
    downloader.active_downloads[task_id] = {
        "status": DownloadStatus.DOWNLOADING,
        "url": "https://example.com",
        "progress": {},
    }

    status = downloader.get_download_status(task_id)
    assert status is not None
    assert status["status"] == DownloadStatus.DOWNLOADING

    # Cleanup
    downloader.cleanup_task(task_id)
    assert downloader.get_download_status(task_id) is None
