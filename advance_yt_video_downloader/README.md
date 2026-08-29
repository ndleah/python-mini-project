# YOUTUBE PLAYLIST/VIDEO DOWNLOADER

A Python CLI tool that downloads entire YouTube playlists or single videos in the highest quality possible, with automatic merging of video and audio streams (if ffmpeg is installed). Built on yt-dlp -- fast, reliable, and actively maintained.

## FEATURES

* * * * *

-   Download entire playlists or single videos with one command.

-   Highest quality -- selects the best video + best audio streams and merges them into a single MP4 (requires ffmpeg).

-   Fallback to H.264 -- force a lighter, widely‑compatible codec to avoid playback lag.

-   Limit the number of videos downloaded from a playlist.

-   Skip existing files -- no duplicate downloads.

-   Progress bar during download.

-   Works with private/unlisted playlists (as long as you have access).

## REQUIREMENTS

* * * * *

-   Python 3.6+

-   yt-dlp -- installed via pip

-   ffmpeg (optional but highly recommended for best quality) -- installed separately

## INSTALLATION

* * * * *

1.  Install Python dependencies:
    ```bash
    pip install yt-dlp
    ```

2.  Install FFmpeg (for merging highest quality streams):

    -   Windows: Download from [gyan.dev](https://gyan.dev/) (choose correct architecture -- 64‑bit or 32‑bit). Extract, then add the bin folder to your system PATH. Verify with: `ffmpeg -version` in a new Command Prompt.

    -   macOS: `brew install ffmpeg`

    -   Linux (Debian/Ubuntu): `sudo apt update && sudo apt install ffmpeg`

    -   Linux (Fedora): `sudo dnf install ffmpeg`

    Without ffmpeg, the script falls back to a single‑stream format (usually 720p or lower). For maximum quality, install it.

## USAGE

* * * * *

`python main.py <URL> [options]`

Required argument:
URL -- YouTube video or playlist URL (must contain "list=" for playlists)

Optional arguments:
-o, --output DIR -- Output directory (default: current folder)
-n, --limit N -- Download only the first N videos (playlist only)
-q, --quality Q -- Override format filter (see examples below)
-v, --verbose -- Show detailed download logs

## EXAMPLES

* * * * *

1.  Download an entire playlist (highest quality):
    ```bash
    python main.py "[https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxx](https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxx)" -o ./videos
    ```

2.  Download only the first 5 videos from a playlist:
    ```bash
    python main.py "[https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxx](https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxx)" -n 5 -o ./videos
    ```

3.  Download a single video:
    ```bash
    python main.py "[https://www.youtube.com/watch?v=abc123](https://www.youtube.com/watch?v=abc123)" -o ./videos
    ```

4.  Force 1080p H.264 (smooth playback on any device):
    ```bash
    python main.py "URL" -q "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=1080][vcodec^=avc1]" -o ./videos
    ```

5.  Force 720p H.264 (lightweight, fast download):
    ```bash
    python main.py "URL" -q "bestvideo[height<=720][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=720][vcodec^=avc1]" -o ./videos
    ```

6.  Use verbose mode to debug:
    ```bash
    python main.py "URL" -v
    ```

## HOW IT WORKS

* * * * *

1.  The script fetches the playlist or video metadata.

2.  If ffmpeg is present, it downloads the best video and best audio streams separately, then merges them into an MP4.

3.  If ffmpeg is missing, it falls back to the "best" single‑stream format (quality may be lower).

4.  Videos are saved in a folder named after the playlist (or "Videos/" for single videos) inside your output directory.

## TROUBLESHOOTING

* * * * *

-   Only 1 video downloads: Make sure your URL contains "&list=" or is the "/playlist?list=" page -- you are probably pointing to a single video.

-   Error: 'list' is not recognized: You forgot to put the URL in double quotes. Always wrap the URL in quotes on Windows.

-   Video lags in VLC: You are likely playing a VP9 or HEVC (H.265) video that your hardware can't decode. Fix: Force H.264 with the -q filter (see examples above) or enable hardware acceleration in VLC (Tools -> Preferences -> Input/Codecs -> Video codecs -> FFmpeg -> Hardware decoding -> DirectX/D3D11).

-   ffmpeg not found: Install FFmpeg and add it to your system PATH. Restart your terminal after installation.

-   Can't delete downloaded videos: Close VLC and any other media player. Then use the command: `rmdir /s /q "folder_path"` (Windows) or `rm -rf folder_path` (macOS/Linux).

## LICENSE

* * * * *

This script is free to use and modify. No warranty -- use at your own risk.

## ACKNOWLEDGEMENTS

* * * * *

-   yt-dlp (https://github.com/yt-dlp/yt-dlp) -- the powerhouse behind the downloads.

-   FFmpeg (https://ffmpeg.org/) -- for merging streams.

This script and its documentation were created with the assistance of an AI tool (DeepSeek) to ensure clarity and completeness.

Happy downloading!

## REQUIREMENTS

* * * * *

-   Python 3.6+

-   yt-dlp -- installed via pip

-   ffmpeg (optional but highly recommended for best quality) -- installed separately

## INSTALLATION

* * * * *

1.  Install Python dependencies:\
    pip install yt-dlp

2.  Install FFmpeg (for merging highest quality streams):

    -   Windows: Download from [gyan.dev](https://gyan.dev/) (choose correct architecture -- 64‑bit or 32‑bit). Extract, then add the bin folder to your system PATH. Verify with: ffmpeg -version in a new Command Prompt.

    -   macOS: brew install ffmpeg

    -   Linux (Debian/Ubuntu): sudo apt update && sudo apt install ffmpeg

    -   Linux (Fedora): sudo dnf install ffmpeg

    Without ffmpeg, the script falls back to a single‑stream format (usually 720p or lower). For maximum quality, install it.

## USAGE

* * * * *

python main.py <URL> [options]

Required argument:\
URL -- YouTube video or playlist URL (must contain "list=" for playlists)

Optional arguments:\
-o, --output DIR -- Output directory (default: current folder)\
-n, --limit N -- Download only the first N videos (playlist only)\
-q, --quality Q -- Override format filter (see examples below)\
-v, --verbose -- Show detailed download logs

## EXAMPLES

* * * * *

1.  Download an entire playlist (highest quality):\
```bash
    python main.py "<https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxx>" -o ./videos
```
2.  Download only the first 5 videos from a playlist:\
```bash
    python main.py "<https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxx>" -n 5 -o ./videos
```
3.  Download a single video:\
```bash
    python main.py "<https://www.youtube.com/watch?v=abc123>" -o ./videos
```
4.  Force 1080p H.264 (smooth playback on any device):\
```bash
    python main.py "URL" -q "bestvideo[height<=1080][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=1080][vcodec^=avc1]" -o ./videos
```

5.  Force 720p H.264 (lightweight, fast download):\
```bash
    python main.py "URL" -q "bestvideo[height<=720][vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[height<=720][vcodec^=avc1]" -o ./videos
```

6.  Use verbose mode to debug:\
```bash
    python main.py "URL" -v
```

## HOW IT WORKS

* * * * *

1.  The script fetches the playlist or video metadata.

2.  If ffmpeg is present, it downloads the best video and best audio streams separately, then merges them into an MP4.

3.  If ffmpeg is missing, it falls back to the "best" single‑stream format (quality may be lower).

4.  Videos are saved in a folder named after the playlist (or "Videos/" for single videos) inside your output directory.

## TROUBLESHOOTING

* * * * *

-   Only 1 video downloads: Make sure your URL contains "&list=" or is the "/playlist?list=" page -- you are probably pointing to a single video.

-   Error: 'list' is not recognized: You forgot to put the URL in double quotes. Always wrap the URL in quotes on Windows.

-   Video lags in VLC: You are likely playing a VP9 or HEVC (H.265) video that your hardware can't decode. Fix: Force H.264 with the -q filter (see examples above) or enable hardware acceleration in VLC (Tools -> Preferences -> Input/Codecs -> Video codecs -> FFmpeg -> Hardware decoding -> DirectX/D3D11).

-   ffmpeg not found: Install FFmpeg and add it to your system PATH. Restart your terminal after installation.

-   Can't delete downloaded videos: Close VLC and any other media player. Then use the command: rmdir /s /q "folder_path" (Windows) or rm -rf folder_path (macOS/Linux).

## LICENSE

* * * * *

This script is free to use and modify. No warranty -- use at your own risk.

## ACKNOWLEDGEMENTS

* * * * *

-   yt-dlp (<https://github.com/yt-dlp/yt-dlp>) -- the powerhouse behind the downloads.

-   FFmpeg (<https://ffmpeg.org/>) -- for merging streams.

This script and its documentation were created with the assistance of an AI tool (DeepSeek) to ensure clarity and completeness.

Happy downloading!

* * * * *