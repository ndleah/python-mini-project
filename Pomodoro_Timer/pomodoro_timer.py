"""A dependency-free command-line Pomodoro timer."""

import argparse
import time
from typing import Callable


def positive_int(value: str) -> int:
    """Parse a positive integer for an argparse option."""
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a whole number") from exc
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def countdown(seconds: int, label: str, sleep: Callable[[float], None] = time.sleep) -> None:
    """Print a once-per-second countdown for the requested interval."""
    print(f"\n{label} — time to focus!" if "Focus" in label else f"\n{label}")
    try:
        for remaining in range(seconds, 0, -1):
            minutes, secs = divmod(remaining, 60)
            print(f"\rTime remaining: {minutes:02d}:{secs:02d}", end="", flush=True)
            sleep(1)
    except KeyboardInterrupt:
        print("\nTimer stopped.")
        raise
    print("\rTime is up!              ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A simple command-line Pomodoro timer.")
    parser.add_argument("--work", type=positive_int, default=25, help="focus interval in minutes (default: 25)")
    parser.add_argument("--short-break", type=positive_int, default=5, help="short break in minutes (default: 5)")
    parser.add_argument("--long-break", type=positive_int, default=15, help="long break in minutes (default: 15)")
    parser.add_argument("--cycles", type=positive_int, default=4, help="number of focus intervals (default: 4)")
    return parser.parse_args()


def run_timer(work: int, short_break: int, long_break: int, cycles: int) -> None:
    """Run the requested number of focus intervals and breaks."""
    try:
        for cycle in range(1, cycles + 1):
            print(f"\nCycle {cycle} of {cycles}")
            countdown(work * 60, "Focus session")
            if cycle < cycles:
                is_long_break = cycle % 4 == 0
                break_minutes = long_break if is_long_break else short_break
                break_name = "Long break" if is_long_break else "Short break"
                countdown(break_minutes * 60, f"{break_name} — relax")
    except KeyboardInterrupt:
        return
    print("\nAll done — great work! 🎉")


def main() -> None:
    args = parse_args()
    run_timer(args.work, args.short_break, args.long_break, args.cycles)


if __name__ == "__main__":
    main()
