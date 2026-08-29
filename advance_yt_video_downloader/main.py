#!/usr/bin/env python3
"""
YouTube Playlist/Video Downloader – Highest Quality with FFmpeg.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("ERROR: yt-dlp is not installed. Run: pip install yt-dlp")
    sys.exit(1)

def check_ffmpeg():
    """Return True if ffmpeg is available and working."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True, timeout=5)
        return True
    except (subprocess.SubprocessError, FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return False

def get_playlist_info(url):
    with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                return info.get('title', 'Playlist'), len(info['entries'])
            else:
                return None, 1
        except Exception as e:
            print(f"Could not fetch playlist info: {e}")
            return None, 1

def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').strip()
        s = d.get('_speed_str', 'N/A').strip()
        e = d.get('_eta_str', 'N/A').strip()
        print(f"\rDownloading: {p} at {s}, ETA: {e}", end='')
    elif d['status'] == 'finished':
        print("\nDownload completed, now processing...")

def download_playlist(url, output_dir, limit=None, quality=None):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Check for ffmpeg
    has_ffmpeg = check_ffmpeg()
    if not has_ffmpeg:
        print("  ffmpeg is not installed or not working properly!")
        print("   Without ffmpeg, we cannot merge separate video+audio streams.")
        print("   Falling back to 'best' format (a single stream, may be lower quality).")
        print("   For best quality, install ffmpeg from https://ffmpeg.org/ and add it to PATH.\n")
        if quality is None:
            quality = "best"
    else:
        print(" ffmpeg found – will merge best video and audio streams.\n")
        if quality is None:
            quality = "bestvideo+bestaudio/best"

    # Get playlist info
    playlist_title, count = get_playlist_info(url)
    if playlist_title:
        safe_title = "".join(c for c in playlist_title if c.isalnum() or c in " -_").strip() or "Playlist"
        subfolder = safe_title
        outtmpl = os.path.join(output_dir, subfolder, '%(playlist_index)s - %(title)s.%(ext)s')
        print(f" Playlist: {playlist_title} ({count} videos)")
    else:
        subfolder = "Videos"
        outtmpl = os.path.join(output_dir, subfolder, '%(title)s.%(ext)s')
        print(" Single video download")

    ydl_opts = {
        'format': quality,
        'outtmpl': outtmpl,
        'merge_output_format': 'mp4',
        'ignoreerrors': True,
        'nooverwrites': True,
        'quiet': False,
        'progress_hooks': [progress_hook],
    }

    if limit and playlist_title:
        ydl_opts['playlistend'] = limit
        print(f" Limiting to first {limit} videos")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"\n Fetching: {url}\n")
            ydl.download([url])
            print("\n All downloads completed!")
        except Exception as e:
            print(f"\n An error occurred: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Download YouTube playlist/video in highest quality.")
    parser.add_argument("url", help="Playlist or video URL (must include 'list=' for playlists)")
    parser.add_argument("-o", "--output", default=".", help="Output directory (default: current)")
    parser.add_argument("-n", "--limit", type=int, help="Max number of videos to download (playlist only)")
    parser.add_argument("-q", "--quality", default=None, help="Override format (e.g., 'bestvideo[height<=1080]+bestaudio')")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debug logs")
    args = parser.parse_args()

    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    download_playlist(args.url, args.output, args.limit, args.quality)

if __name__ == "__main__":
    main()