import os
import pytube
from moviepy.editor import AudioFileClip

def main():
    print("=== YouTube Audio Downloader ===")
    
    # Get YouTube URL from user
    youtube_url = input("Enter YouTube video URL: ").strip()
    if not youtube_url:
        print("Error: URL cannot be empty.")
        return

    # Get output directory
    output_dir = input("Enter save directory path (press Enter for current directory): ").strip()
    if not output_dir:
        output_dir = "."
    
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
        except Exception as e:
            print(f"Error creating directory '{output_dir}': {e}")
            return

    # Get file name
    file_name = input("Enter output filename (e.g. audio.mp3 or press Enter for default 'audio.mp3'): ").strip()
    if not file_name:
        file_name = "audio.mp3"
    elif not file_name.endswith(".mp3"):
        file_name += ".mp3"

    target_path = os.path.join(output_dir, file_name)

    try:
        print("Fetching video streams...")
        yt = pytube.YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not audio_stream:
            print("Error: No audio stream found for this video.")
            return

        print("Downloading audio stream...")
        temp_file = audio_stream.download()

        print("Converting audio to MP3...")
        audio_clip = AudioFileClip(temp_file)
        audio_clip.write_audiofile(target_path)
        audio_clip.close()

        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

        print(f"\nSuccess! Audio saved as MP3 file to: {os.path.abspath(target_path)}")

    except Exception as e:
        print(f"\nAn error occurred while processing the video: {e}")

if __name__ == "__main__":
    main()