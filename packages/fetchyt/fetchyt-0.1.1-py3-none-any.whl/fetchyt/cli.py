"""Command-line interface for FetchYT.

Copyright (c) Krishnakanth Allika
License: CC-BY-NC-SA-4.0
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional

from .downloader import YouTubeDownloader
from .config import settings


def print_header():
    """Print CLI header."""
    print("=" * 60)
    print("🎵 FetchYT - YouTube Playlist Downloader")
    print(f"Version {settings.APP_VERSION}")
    print("=" * 60)
    print()


def print_video_info(videos):
    """Print video information.

    Args:
        videos: List of VideoInfo objects
    """
    print(f"\n📋 Found {len(videos)} video(s):\n")
    for i, video in enumerate(videos, 1):
        duration = (
            f"{video.duration // 60}:{video.duration % 60:02d}"
            if video.duration
            else "Unknown"
        )
        print(f"{i}. {video.title}")
        print(f"   Uploader: {video.uploader or 'Unknown'} | Duration: {duration}")
        print()


async def download_command(args):
    """Handle download command.

    Args:
        args: Command-line arguments
    """
    print_header()

    # Initialize downloader
    download_dir = Path(args.output) if args.output else settings.ensure_download_dir()
    downloader = YouTubeDownloader(download_dir)

    print(f"📁 Download directory: {download_dir.absolute()}\n")

    # Extract information
    print(f"🔍 Extracting information from: {args.url}")
    try:
        videos = await downloader.extract_info(args.url)
        print_video_info(videos)
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error extracting info:\n", file=sys.stderr)
        print(error_msg, file=sys.stderr)
        return 1

    # Confirm download if not in yes mode
    if not args.yes:
        response = input(
            f"Download {len(videos)} video(s) as {args.format.upper()}? [y/N]: "
        )
        if response.lower() not in ["y", "yes"]:
            print("❌ Download cancelled")
            return 0

    # Start download
    print(f"\n⬇️  Downloading to {download_dir}...")
    print(f"Format: {args.format.upper()} | Quality: {args.quality} kbps\n")

    try:
        task_id = await downloader.download(
            url=args.url,
            format=args.format,
            quality=args.quality,
        )

        # Wait for completion
        while True:
            status = downloader.get_download_status(task_id)
            if not status:
                break

            if status["status"] == "completed":
                print("\n✅ Download completed successfully!")
                break
            elif status["status"] == "failed":
                error = status.get("error", "Unknown error")
                print(f"\n❌ Download failed: {error}", file=sys.stderr)
                return 1

            await asyncio.sleep(1)

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Download error: {e}", file=sys.stderr)
        return 1


async def info_command(args):
    """Handle info command.

    Args:
        args: Command-line arguments
    """
    print_header()

    downloader = YouTubeDownloader()

    print(f"🔍 Extracting information from: {args.url}\n")
    try:
        videos = await downloader.extract_info(args.url)
        print_video_info(videos)

        # Summary
        total_duration = sum(v.duration or 0 for v in videos)
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60
        print(f"📊 Total: {len(videos)} video(s), {hours}h {minutes}m")

        return 0
    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error:\n", file=sys.stderr)
        print(error_msg, file=sys.stderr)
        return 1


async def server_command(args):
    """Handle server command.

    Args:
        args: Command-line arguments
    """
    import uvicorn
    from .api import app

    print_header()
    print(f"🚀 Starting FastAPI server...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   Web Interface: http://{args.host}:{args.port}")
    print(f"   API Docs: http://{args.host}:{args.port}/docs")
    print()

    config = uvicorn.Config(
        app=app,
        host=args.host,
        port=args.port,
        log_level="info",
    )
    server = uvicorn.Server(config)

    await server.serve()


def cookies_command(args):
    """Handle cookies command to extract browser cookies.

    Args:
        args: Command-line arguments
    """
    print_header()

    print(f"🍪 Extracting cookies from {args.browser.capitalize()}...")
    print(
        f"   Make sure {args.browser.capitalize()} is open and you're logged into YouTube\n"
    )

    try:
        cookies_path = YouTubeDownloader.extract_cookies_from_browser(
            browser=args.browser,
            output_file=Path(args.output),
        )

        print(f"✅ Successfully extracted cookies!")
        print(f"   Saved to: {cookies_path.absolute()}\n")

        print(f"📝 To use these cookies with FetchYT:")
        print(f"   export COOKIES_FILE={cookies_path.absolute()}")
        print(f"\n   Then run:")
        print(f"   fetchyt info <URL>")
        print(f"   fetchyt download <URL>")

        return 0

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error extracting cookies:\n", file=sys.stderr)
        print(error_msg, file=sys.stderr)
        return 1

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FetchYT - Download MP3s from YouTube playlists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
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
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"FetchYT {settings.APP_VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Download command
    download_parser = subparsers.add_parser(
        "download",
        help="Download video(s) from YouTube",
    )
    download_parser.add_argument(
        "url",
        help="YouTube video or playlist URL",
    )
    download_parser.add_argument(
        "-f",
        "--format",
        default="mp3",
        choices=["mp3", "m4a", "wav"],
        help="Audio format (default: mp3)",
    )
    download_parser.add_argument(
        "-q",
        "--quality",
        default="192",
        choices=["128", "192", "256", "320"],
        help="Audio quality in kbps (default: 192)",
    )
    download_parser.add_argument(
        "-o",
        "--output",
        help="Output directory (default: ./downloads)",
    )
    download_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )

    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Get information about video(s) without downloading",
    )
    info_parser.add_argument(
        "url",
        help="YouTube video or playlist URL",
    )

    # Server command
    server_parser = subparsers.add_parser(
        "server",
        help="Start the FastAPI web server",
    )
    server_parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Server host (default: 0.0.0.0)",
    )
    server_parser.add_argument(
        "--port",
        type=int,
        default=settings.API_PORT,
        help=f"Server port (default: {settings.API_PORT})",
    )

    # Cookies command
    cookies_parser = subparsers.add_parser(
        "cookies",
        help="Extract cookies from browser for YouTube authentication",
    )
    cookies_parser.add_argument(
        "-b",
        "--browser",
        default="chrome",
        choices=["chrome", "firefox", "edge", "safari", "opera", "brave"],
        help="Browser to extract cookies from (default: chrome)",
    )
    cookies_parser.add_argument(
        "-o",
        "--output",
        default="cookies.txt",
        help="Output file for cookies (default: cookies.txt)",
    )

    args = parser.parse_args()

    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 0

    # Execute command
    try:
        if args.command == "download":
            return asyncio.run(download_command(args))
        elif args.command == "info":
            return asyncio.run(info_command(args))
        elif args.command == "server":
            return asyncio.run(server_command(args))
        elif args.command == "cookies":
            return cookies_command(args)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Fatal error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
