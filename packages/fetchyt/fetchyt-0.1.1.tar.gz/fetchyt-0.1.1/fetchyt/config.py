"""Configuration settings for FetchYT.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

import os
from pathlib import Path
from typing import Optional


class Settings:
    """Application settings."""

    # Application
    APP_NAME: str = "FetchYT"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8098"))
    API_PREFIX: str = "/api/v1"

    # Downloads
    DOWNLOAD_DIR: Path = Path(os.getenv("DOWNLOAD_DIR", "downloads"))
    MAX_CONCURRENT_DOWNLOADS: int = int(os.getenv("MAX_CONCURRENT_DOWNLOADS", "3"))

    # YouTube DL Options
    YOUTUBE_DL_FORMAT: str = "bestaudio/best"
    AUDIO_FORMAT: str = "mp3"
    AUDIO_QUALITY: str = "192"  # kbps
    COOKIES_FILE: Optional[Path] = (
        Path(os.getenv("COOKIES_FILE")) if os.getenv("COOKIES_FILE") else None
    )

    # CORS
    CORS_ORIGINS: list = ["*"]  # Configure this for production

    @classmethod
    def ensure_download_dir(cls) -> Path:
        """Ensure download directory exists."""
        cls.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        return cls.DOWNLOAD_DIR


settings = Settings()
