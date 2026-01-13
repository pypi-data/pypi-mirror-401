# FetchYT 🎵

Download MP3s from YouTube playlists with a modern web interface and CLI tool.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC--BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Features

- 📥 **Download MP3s** from YouTube videos and playlists
- 🌐 **Web Interface** with dark mode design
- 🖥️ **CLI Tool** for terminal usage
- 🚀 **FastAPI Backend** for scalability
- 📦 **Easy Installation** via PyPI
- 🎨 **Multiple Format Support** (MP3, M4A, WAV)
- ⚡ **Quality Options** (128, 192, 256, 320 kbps)

## Installation

### From PyPI

```bash
# Using uv (recommended - faster)
uv pip install fetchyt

# Or using pip
pip install fetchyt
```

### From Source

```bash
git clone https://gitlab.com/allikapub/fetchyt.git
cd fetchyt

# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

### Development Setup

```bash
# Clone the repository
git clone https://gitlab.com/allikapub/fetchyt.git
cd fetchyt

# Using uv (recommended - much faster)
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

## Quick Start

### CLI Usage

```bash
# Download a single video
fetchyt download "https://www.youtube.com/watch?v=VIDEO_ID"

# Download a playlist
fetchyt download "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Download with custom quality and format
fetchyt download "URL" --format m4a --quality 320

# Get information without downloading
fetchyt info "URL"

# Start web server
fetchyt server --port 8098
```

### Web Interface

Start the web server:

```bash
fetchyt server
```

Then open your browser and navigate to `http://localhost:8098`

### Python API

```python
import asyncio
from fetchyt import YouTubeDownloader

async def main():
    downloader = YouTubeDownloader()
    
    # Extract information
    videos = await downloader.extract_info("YOUTUBE_URL")
    print(f"Found {len(videos)} videos")
    
    # Download
    task_id = await downloader.download(
        url="YOUTUBE_URL",
        format="mp3",
        quality="192"
    )
    print(f"Download started: {task_id}")

asyncio.run(main())
```

## CLI Commands

### Download Command

```bash
fetchyt download <URL> [OPTIONS]

Options:
  -f, --format    Audio format: mp3, m4a, wav (default: mp3)
  -q, --quality   Audio quality: 128, 192, 256, 320 kbps (default: 192)
  -o, --output    Output directory (default: ./downloads)
  -y, --yes       Skip confirmation prompt
```

### Info Command

```bash
fetchyt info <URL>
```

Get information about videos without downloading.

### Cookies Command

Extract YouTube cookies directly from your browser to bypass bot detection:

```bash
# Chrome/Chromium
fetchyt cookies --browser chrome --output cookies.txt

# Firefox
fetchyt cookies --browser firefox --output cookies.txt

# Use the cookies in FetchYT
# PowerShell (Windows)
$env:COOKIES_FILE = "./cookies.txt"
# bash (Linux/macOS)
export COOKIES_FILE=./cookies.txt

# Then run
fetchyt info "<URL>"
fetchyt download "<URL>"
```

### Server Command

  print(f"Download started: {task_id}")

asyncio.run(main())
Options:
  --host    Server host (default: 0.0.0.0)
  --port    Server port (default: 8098)
```

## API Endpoints

When running as a server, FetchYT provides the following REST API endpoints:

- `GET /` - Web interface
- `POST /api/v1/extract` - Extract video/playlist information
- `POST /api/v1/download` - Start download
- `GET /api/v1/status/{task_id}` - Check download status
- `DELETE /api/v1/task/{task_id}` - Cleanup completed task
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

## Using uv (Recommended)

This project supports **uv**, a blazingly fast Python package installer (10-100x faster than pip). The setup scripts will automatically install and use uv. For detailed uv usage, see [UV_GUIDE.md](UV_GUIDE.md).

## Configuration

FetchYT can be configured using environment variables:

```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8098

# Download Configuration
export DOWNLOAD_DIR=./downloads
export MAX_CONCURRENT_DOWNLOADS=3
export COOKIES_FILE=./cookies.txt   # Optional: path to exported browser cookies

# Debug Mode
export DEBUG=True
```

## Project Structure

```
fetchyt/
├── fetchyt/
│   ├── __init__.py          # Package initialization
│   ├── api.py               # FastAPI application
│   ├── cli.py               # Command-line interface
│   ├── config.py            # Configuration settings
│   ├── downloader.py        # YouTube downloader core
│   ├── models.py            # Data models
│   └── static/              # Web interface
│       ├── index.html
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Requirements

- Python 3.12+
- FFmpeg (for audio conversion)
- **uv** (recommended) or pip for package management
- yt-dlp (installed automatically as a dependency)

## Troubleshooting (YouTube bot detection)

If you see an error like "Sign in to confirm you’re not a bot":

- Extract cookies from your browser and set `COOKIES_FILE` (see Cookies Command above)
- Wait 10–30 minutes and try again (temporary rate limits)
- Try a different network or a VPN
- Use a different browser to export cookies

Learn more: https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies

### Installing uv (Recommended)

**uv** is a blazingly fast Python package installer and resolver:

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Learn more: https://github.com/astral-sh/uv

### Installing FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

## Development

### Running Tests

```bash
pytest
```

## Publishing to PyPI

### Prerequisites

1. Install build tools:
```bash
pip install build twine
```

2. Create accounts on [PyPI](https://pypi.org) and [TestPyPI](https://test.pypi.org)

### Build and Upload

```bash
# Build the package
python -m build

# Upload to TestPyPI (for testing)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI (production)
python -m twine upload dist/*
```

## Roadmap

- [ ] Resume interrupted downloads
- [ ] Batch download from file
- [ ] Download queue management
- [ ] Progress notifications
- [ ] Subtitle download support
- [ ] Video format support
- [ ] Playlist filtering options
- [ ] Docker support
- [ ] Desktop application (Electron/Tauri)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. See [LICENSE](LICENSE) for details.

## Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Always ensure you have the right to download content.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful YouTube downloader
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [FFmpeg](https://ffmpeg.org/) - Multimedia framework

## Support

If you encounter any issues or have questions:

- 🐛 [Report a bug](https://gitlab.com/allikapub/fetchyt/-/issues)
- 💡 [Request a feature](https://gitlab.com/allikapub/fetchyt/-/issues)
- 💬 [Start a discussion](https://gitlab.com/allikapub/fetchyt/-/discussions)

---

Made with ❤️ by the FetchYT team

Copyright (c) 2026 Krishnakanth Allika. All rights reserved.

Licensed under [CC-BY-NC-SA-4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
