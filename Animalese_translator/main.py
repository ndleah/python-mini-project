import os
import sys

def generate_animalese(
    text: str = "Hello Animalese",
    voice_dir: str = None,
    output_path: str = None,
    speed_multiplier: float = 2.2,
    play_audio: bool = False
) -> str:
    """Generate Animalese audio speech WAV file from input text."""
    script_dir = os.path.dirname(__file__)

    if voice_dir is None:
        voice_dir = os.path.join(script_dir, "voices", "guy3")

    if not os.path.exists(voice_dir):
        print(f"Error: Voice samples directory not found at '{voice_dir}'")
        return None

    try:
        from scipy.io import wavfile
        from scipy.io.wavfile import write
        import numpy as np
    except ImportError:
        print("Notice: scipy / numpy libraries not installed.")
        return None

    files = [f for f in os.listdir(voice_dir) if f.lower().endswith('.wav')]
    files.sort()

    sounds = {}
    sample_rate = 48000
    for file in files:
        raw_name = file.split(".")[0]
        fp = os.path.join(voice_dir, file)
        try:
            rate, data = wavfile.read(fp)
            sample_rate = rate
            channel_one = data[:, 0] if len(data.shape) > 1 else data
            sounds[raw_name] = channel_one
        except Exception as e:
            print(f"Skipping audio sample '{file}': {e}")

    if not sounds:
        print("Error: No valid WAV samples loaded.")
        return None

    say = text.lower().strip()
    advance = 0.15 * sample_rate
    space_skip = 0.4 * advance

    cursor = 0.0
    notes = []
    for char in say:
        if char in sounds:
            notes.append((char, cursor))
            cursor += advance
        elif char == " ":
            cursor += space_skip

    if not notes:
        print("Notice: No matching character sounds found for input string.")
        return None

    last_char = notes[-1][0]
    last_note = sounds[last_char]
    last_note_length = last_note.shape[0]
    total_duration = cursor + last_note_length

    end_pad = sample_rate * 1.0
    buffer_length = int(total_duration + end_pad)
    base = np.zeros(buffer_length, dtype=np.int16)

    for char, cur in notes:
        sound = sounds[char]
        start = int(cur)
        end = int(start + sound.shape[0])
        base[start:end] += sound

    if output_path is None:
        output_dir = os.path.join(script_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        filename = text.replace(" ", "_").lower() + ".wav"
        output_path = os.path.join(output_dir, filename)

    write_rate = int(sample_rate * speed_multiplier)
    write(output_path, write_rate, base.astype(np.int16))
    print(f"Animalese audio synthesized successfully -> '{output_path}'")

    if play_audio:
        try:
            from playsound import playsound
            playsound(output_path)
        except Exception:
            print("Notice: playsound library or audio playback device unavailable.")

    return output_path

def main():
    target_text = sys.argv[1] if len(sys.argv) > 1 else "Hello Animalese"
    generate_animalese(target_text)

if __name__ == '__main__':
    main()

