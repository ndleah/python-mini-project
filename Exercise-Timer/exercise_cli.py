import os
import sys
import time as t
from pathlib import Path
import click

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

BASE_DIR = Path(__file__).resolve().parent

def load_sounds():
    """Initializes pygame mixer and preloads audio files using absolute paths."""
    sounds = {}
    try:
        pygame.mixer.init()
        sound_files = {
            "start": "beep_start.mp3",
            "stop": "beep_stop.mp3",
            "finish": "beep_finish.mp3",
        }
        for key, filename in sound_files.items():
            filepath = BASE_DIR / filename
            if filepath.exists():
                sounds[key] = pygame.mixer.Sound(str(filepath))
            else:
                sounds[key] = None
    except Exception:
        # Fallback gracefully if audio device is unavailable
        sounds = {"start": None, "stop": None, "finish": None}
    return sounds

def play_audio(sound, wait_factor: float = 1.0):
    """Plays an audio sound and waits for its duration."""
    if sound is not None:
        try:
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000 * wait_factor))
        except Exception:
            pass

def countdown_timer(seconds: int, stage_label: str):
    """Displays a live terminal countdown timer."""
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"\r  ?? [{stage_label}] {mins:02d}:{secs:02d} remaining...", end="", flush=True)
        t.sleep(1)
    print("\r" + " " * 50 + "\r", end="", flush=True)

@click.command()
@click.option('--time', '-t', default=10, type=click.IntRange(min=1), help='Time you want to exercise (in seconds)')
@click.option('--interval', '-i', default=3, type=click.IntRange(min=1), help='Interval rest time between reps (in seconds)')
@click.option('--reps', '-r', default=5, type=click.IntRange(min=1), help='Number of reps you want to do')
@click.option('--prep', '-p', default=3, type=click.IntRange(min=0), help='Preparation time before starting workout (in seconds)')
def exercise(time: int, interval: int, reps: int, prep: int):
    """CLI Exercise Timer with audio cues and interval tracking."""
    sounds = load_sounds()

    print("\n==============================")
    print("      ??? EXERCISE TIMER       ")
    print("==============================")
    print(f"Total Reps: {reps} | Work: {time}s | Rest: {interval}s | Prep: {prep}s\n")

    try:
        if prep > 0:
            print("?? Get Ready!")
            countdown_timer(prep, "Preparation")

        for current_rep in range(1, reps + 1):
            print(f"\n--- Rep {current_rep}/{reps} ---")
            print("?? Start Exercise!")
            play_audio(sounds.get("start"))
            countdown_timer(time, f"Rep {current_rep}/{reps} [Work]")

            print("?? Stop!")
            play_audio(sounds.get("stop"))

            reps_remaining = reps - current_rep
            if reps_remaining > 0:
                print(f"? Rest Interval ({reps_remaining} rep{'s' if reps_remaining > 1 else ''} left)")
                countdown_timer(interval, "Rest Interval")
            else:
                print("\n?? Workout Finished! Excellent effort! ??")
                play_audio(sounds.get("finish"), wait_factor=1.5)

    except KeyboardInterrupt:
        print("\n\n?? Workout stopped by user. Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    exercise()
