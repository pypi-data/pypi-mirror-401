"""FastAPI application for FetchYT.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

import asyncio
from pathlib import Path
from typing import Dict
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .downloader import YouTubeDownloader
from .models import (
    DownloadRequest,
    DownloadResponse,
    DownloadStatusResponse,
    DownloadStatus,
    DownloadProgress,
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Download MP3s from YouTube playlists",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize downloader
downloader = YouTubeDownloader()

# Track active tasks
active_tasks: Dict[str, Dict] = {}


@app.get("/")
async def root():
    """Root endpoint - serves the web interface."""
    frontend_path = Path(__file__).parent / "static" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    return {"message": "FetchYT API", "version": settings.APP_VERSION}


@app.post(f"{settings.API_PREFIX}/extract", response_model=DownloadResponse)
async def extract_info(request: DownloadRequest):
    """Extract information from YouTube URL without downloading.

    Args:
        request: Download request containing URL

    Returns:
        Video/playlist information
    """
    try:
        videos = await downloader.extract_info(request.url)
        return DownloadResponse(
            task_id="",
            status=DownloadStatus.PENDING,
            message=f"Found {len(videos)} video(s)",
            videos=videos,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract info: {str(e)}")


@app.post(f"{settings.API_PREFIX}/download", response_model=DownloadResponse)
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    """Start downloading from YouTube URL.

    Args:
        request: Download request containing URL and options
        background_tasks: FastAPI background tasks

    Returns:
        Download response with task ID
    """
    try:
        # Extract video info first
        videos = await downloader.extract_info(request.url)

        # Start download in background
        async def download_task():
            await downloader.download(
                url=request.url,
                format=request.format,
                quality=request.quality,
            )

        # Generate task ID and start download
        import uuid

        task_id = str(uuid.uuid4())
        active_tasks[task_id] = {
            "status": DownloadStatus.DOWNLOADING,
            "videos": videos,
            "total": len(videos),
            "completed": 0,
        }

        # Schedule the download
        background_tasks.add_task(download_task)

        return DownloadResponse(
            task_id=task_id,
            status=DownloadStatus.DOWNLOADING,
            message=f"Started downloading {len(videos)} video(s)",
            videos=videos,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to start download: {str(e)}"
        )


@app.get(
    f"{settings.API_PREFIX}/status/{{task_id}}", response_model=DownloadStatusResponse
)
async def get_download_status(task_id: str):
    """Get status of a download task.

    Args:
        task_id: Task identifier

    Returns:
        Download status information
    """
    if task_id not in active_tasks:
        # Check downloader's active downloads
        status = downloader.get_download_status(task_id)
        if not status:
            raise HTTPException(status_code=404, detail="Task not found")

        # Convert to response format
        progress_list = [prog for prog in status.get("progress", {}).values()]
        completed = sum(
            1 for p in progress_list if p.status == DownloadStatus.COMPLETED
        )

        return DownloadStatusResponse(
            task_id=task_id,
            status=status.get("status", DownloadStatus.PENDING),
            progress=progress_list,
            completed=completed,
            total=len(progress_list),
        )

    task = active_tasks[task_id]
    return DownloadStatusResponse(
        task_id=task_id,
        status=task.get("status", DownloadStatus.PENDING),
        progress=[],
        completed=task.get("completed", 0),
        total=task.get("total", 0),
    )


@app.delete(f"{settings.API_PREFIX}/task/{{task_id}}")
async def cleanup_task(task_id: str):
    """Clean up a completed or failed task.

    Args:
        task_id: Task identifier

    Returns:
        Success message
    """
    if task_id in active_tasks:
        del active_tasks[task_id]

    downloader.cleanup_task(task_id)

    return {"message": "Task cleaned up successfully"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "active_downloads": len(downloader.active_downloads),
    }


# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "fetchyt.api:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
