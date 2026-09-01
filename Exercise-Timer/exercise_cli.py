import os
import sys
import time as t
import click

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def get_audio_path(filename: str) -> str:
    """Resolve sound file path relative to script directory."""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, filename)

def play_sound(filename: str, duration_sec: float = 1.0):
    """Play audio file via pygame mixer or console audio fallback."""
    sound_path = get_audio_path(filename)
    try:
        import pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if os.path.exists(sound_path):
            sound = pygame.mixer.Sound(sound_path)
            sound.play()
            pygame.time.wait(int(sound.get_length() * 1000))
            return
    except Exception as e:
        pass

    # Audio fallback: terminal bell
    print('\a', end='', flush=True)

@click.command()
@click.option('--time', '-t', default=10, help='Exercise duration per rep (seconds)')
@click.option('--interval', '-i', default=3, help='Rest interval duration (seconds)')
@click.option('--reps', '-r', default=5, help='Number of reps to perform')
def exercise(time: int, interval: int, reps: int):
    """CLI Exercise & Workout Interval Timer."""
    print(f"\n🏋️ Starting Exercise Timer ({reps} reps, {time}s work, {interval}s rest)...")

    for rep in range(1, reps + 1):
        print(f"\n--- Rep {rep}/{reps} ---")
        print("Rest Interval...")
        t.sleep(interval)

        print("🚀 START Work!")
        play_sound("beep_start.mp3")
        t.sleep(time)

        print("🛑 STOP Work!")
        play_sound("beep_stop.mp3")

        reps_remaining = reps - rep
        if reps_remaining > 0:
            print(f"Reps remaining: {reps_remaining}")
        else:
            print("\n🎉 Workout Finished! Excellent effort!")
            play_sound("beep_finish.mp3", duration_sec=1.5)

def main():
    exercise()

if __name__ == '__main__':
    main()

