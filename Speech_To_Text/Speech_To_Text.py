import os
import sys

def speak_text(command: str):
    """Convert text to speech using pyttsx3."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()
    except Exception as e:
        print(f"Notice: TTS Speech Engine unavailable ({e}). Speech output: '{command}'")

def transcribe_audio_file(audio_file_path: str) -> str:
    """Transcribe speech from an audio file (.wav/.flac)."""
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file '{audio_file_path}' not found.")
        return None

    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.AudioFile(audio_file_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(f"Transcribed Text: {text}")
            return text
    except Exception as e:
        print(f"Error transcribing audio file ({e}).")
        return None

def listen_microphone():
    """Listen to microphone input and convert speech to text."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source2:
            print("\nListening to microphone... Speak now (Press Ctrl+C to stop)")
            r.adjust_for_ambient_noise(source2, duration=0.5)
            audio2 = r.listen(source2)
            my_text = r.recognize_google(audio2).lower()
            print(f"Recognized Speech: {my_text}")
            speak_text(my_text)
            return my_text
    except Exception as e:
        print(f"Microphone input error or missing device: {e}")
        return None

def main():
    print("=== Speech To Text Engine ===")
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        transcribe_audio_file(sys.argv[1])
        return

    try:
        import speech_recognition as sr
        mics = sr.Microphone.list_microphone_names()
        print(f"Available Microphones ({len(mics)}): {mics[:2] if mics else 'None detected'}")
    except Exception:
        print("Notice: speech_recognition / PyAudio library not installed.")
        return

    listen_microphone()

if __name__ == '__main__':
    main()