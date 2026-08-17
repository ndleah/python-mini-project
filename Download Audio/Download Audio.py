import os
import sys

def download_audio(url: str, output_dir: str = "."):
    try:
        import pytube
    except ImportError:
        print("Error: 'pytube' package is required. Install it via 'pip install pytube'.")
        sys.exit(1)

    print(f"Fetching video info from: {url}")
    try:
        yt = pytube.YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            print("Error: No audio stream found for this video.")
            return
    except Exception as e:
        print(f"Error initializing YouTube download: {e}")
        return

    os.makedirs(output_dir, exist_ok=True)

    print("Downloading audio stream...")
    temp_file = audio_stream.download(output_path=output_dir)
    print(f"Audio downloaded: {temp_file}")

    try:
        from moviepy.editor import AudioFileClip
        base, _ = os.path.splitext(temp_file)
        mp3_file = base + ".mp3"
        print(f"Converting to MP3: {mp3_file}")

        audio_clip = AudioFileClip(temp_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()

        if os.path.exists(temp_file) and temp_file != mp3_file:
            os.remove(temp_file)

        print(f"Successfully saved MP3 to: {mp3_file}")
    except ImportError:
        print(f"MoviePy not installed. Downloaded raw audio file: {temp_file}")
    except Exception as e:
        print(f"Notice: MoviePy conversion skipped or failed ({e}). File saved at: {temp_file}")

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
        out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    else:
        url = input("Enter YouTube video URL: ").strip()
        out_dir = "."

    if not url:
        print("Error: No YouTube URL provided.")
        sys.exit(1)

    download_audio(url, out_dir)

if __name__ == "__main__":
    main()