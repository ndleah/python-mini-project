#!/usr/bin/env python3
"""
Conway's Game of Life
=====================
A full-featured simulation of Conway's cellular automaton with:
- Interactive curses UI with colors and responsive resizing
- Fallback ANSI terminal rendering mode for environments without curses
- Multiple pattern presets (Glider, Pulsar, Gosper Gun, Blinker, Beacon, Toad)
- Interactive controls (Pause, Step, Speed, Clear, Randomize, Wrap toggle)
- Decoupled, testable GameOfLifeEngine
"""

import copy
import os
import random
import sys
import time
import argparse
from typing import List, Tuple, Optional

# Optional curses import (with Windows compatibility handling)
try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False


class GameOfLifeEngine:
    """Core simulation engine for Conway's Game of Life."""

    PRESETS = {
        "blinker": [
            (0, 0), (0, 1), (0, 2)
        ],
        "toad": [
            (0, 1), (0, 2), (0, 3),
            (1, 0), (1, 1), (1, 2)
        ],
        "beacon": [
            (0, 0), (0, 1),
            (1, 0),
            (2, 3),
            (3, 2), (3, 3)
        ],
        "glider": [
            (0, 1),
            (1, 2),
            (2, 0), (2, 1), (2, 2)
        ],
        "pulsar": [
            (1, 3), (1, 4), (1, 5), (1, 9), (1, 10), (1, 11),
            (3, 1), (3, 6), (3, 8), (3, 13),
            (4, 1), (4, 6), (4, 8), (4, 13),
            (5, 1), (5, 6), (5, 8), (5, 13),
            (6, 3), (6, 4), (6, 5), (6, 9), (6, 10), (6, 11),
            (8, 3), (8, 4), (8, 5), (8, 9), (8, 10), (8, 11),
            (9, 1), (9, 6), (9, 8), (9, 13),
            (10, 1), (10, 6), (10, 8), (10, 13),
            (11, 1), (11, 6), (11, 8), (11, 13),
            (13, 3), (13, 4), (13, 5), (13, 9), (13, 10), (13, 11)
        ],
        "gosper_gun": [
            (5, 1), (5, 2), (6, 1), (6, 2),
            (5, 11), (6, 11), (7, 11),
            (4, 12), (8, 12),
            (3, 13), (9, 13),
            (3, 14), (9, 14),
            (6, 15),
            (4, 16), (8, 16),
            (5, 17), (6, 17), (7, 17),
            (6, 18),
            (3, 21), (4, 21), (5, 21),
            (3, 22), (4, 22), (5, 22),
            (2, 23), (6, 23),
            (1, 25), (2, 25), (6, 25), (7, 25),
            (3, 35), (4, 35), (3, 36), (4, 36)
        ]
    }

    def __init__(self, rows: int = 20, cols: int = 40, wrap: bool = True):
        self.rows = max(3, rows)
        self.cols = max(3, cols)
        self.wrap = wrap
        self.grid = self._create_grid()
        self.generation = 0

    def _create_grid(self) -> List[List[bool]]:
        return [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def resize(self, rows: int, cols: int):
        """Resize the grid dynamically preserving existing living cells within bounds."""
        new_rows = max(3, rows)
        new_cols = max(3, cols)
        new_grid = [[False for _ in range(new_cols)] for _ in range(new_rows)]
        for r in range(min(self.rows, new_rows)):
            for c in range(min(self.cols, new_cols)):
                new_grid[r][c] = self.grid[r][c]
        self.rows = new_rows
        self.cols = new_cols
        self.grid = new_grid

    def clear(self):
        """Clear all cells and reset generation count."""
        self.grid = self._create_grid()
        self.generation = 0

    def seed_random(self, density: float = 0.25):
        """Seed the grid randomly with the given alive probability."""
        self.generation = 0
        self.grid = [
            [random.random() < density for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

    def load_preset(self, name: str, start_r: Optional[int] = None, start_c: Optional[int] = None) -> bool:
        """Load a predefined pattern into the grid."""
        pattern = self.PRESETS.get(name.lower())
        if not pattern:
            return False

        # Calculate bounding box to center if not specified
        max_pr = max(r for r, _ in pattern)
        max_pc = max(c for _, c in pattern)

        if start_r is None:
            start_r = max(0, (self.rows - max_pr) // 2)
        if start_c is None:
            start_c = max(0, (self.cols - max_pc) // 2)

        self.clear()
        for r, c in pattern:
            target_r = start_r + r
            target_c = start_c + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r][target_c] = True

        return True

    def count_neighbors(self, r: int, c: int) -> int:
        """Count living Moore neighbors for cell (r, c)."""
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.wrap:
                    nr %= self.rows
                    nc %= self.cols
                elif not (0 <= nr < self.rows and 0 <= nc < self.cols):
                    continue

                if self.grid[nr][nc]:
                    count += 1
        return count

    def step(self) -> Tuple[int, int]:
        """
        Advance one generation according to Conway's Game of Life rules:
        1. Any live cell with fewer than two live neighbours dies (underpopulation).
        2. Any live cell with two or three live neighbours lives on to the next generation.
        3. Any live cell with more than three live neighbours dies (overpopulation).
        4. Any dead cell with exactly three live neighbours becomes a live cell (reproduction).

        Returns:
            Tuple of (generation_number, alive_cells_count)
        """
        new_grid = self._create_grid()
        alive_count = 0

        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)
                is_alive = self.grid[r][c]

                if is_alive and (neighbors == 2 or neighbors == 3):
                    new_grid[r][c] = True
                    alive_count += 1
                elif not is_alive and neighbors == 3:
                    new_grid[r][c] = True
                    alive_count += 1

        self.grid = new_grid
        self.generation += 1
        return self.generation, alive_count

    def get_alive_count(self) -> int:
        """Count total alive cells currently on the grid."""
        return sum(row.count(True) for row in self.grid)


def safe_addstr(window, y: int, x: int, text: str, attr: int = 0):
    """Safely draw string avoiding curses boundary overflow exceptions."""
    max_y, max_x = window.getmaxyx()
    if y < 0 or y >= max_y or x < 0 or x >= max_x:
        return
    # Truncate text if it exceeds line width
    available_len = max_x - x
    # If writing to the bottom-right corner, leave 1 character space to prevent auto-scroll error
    if y == max_y - 1:
        available_len = max(0, available_len - 1)
    
    truncated_text = text[:available_len]
    try:
        window.addstr(y, x, truncated_text, attr)
    except curses.error:
        pass


def run_curses_ui(stdscr, preset: str = "random", speed: float = 0.15, wrap: bool = True):
    """Run interactive curses interface."""
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.clear()

    # Color pairs setup
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)     # Living cells
        curses.init_pair(2, curses.COLOR_GREEN, -1)    # Title & controls
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Status bar
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)  # Presets

    height, width = stdscr.getmaxyx()
    grid_rows = max(3, height - 4)
    grid_cols = max(3, width)

    engine = GameOfLifeEngine(rows=grid_rows, cols=grid_cols, wrap=wrap)
    if preset == "random" or preset not in engine.PRESETS:
        engine.seed_random(density=0.25)
    else:
        engine.load_preset(preset)

    paused = False
    current_speed = speed
    status_msg = "Running"

    cell_char = "O"

    while True:
        # Check window resize
        n_height, n_width = stdscr.getmaxyx()
        if n_height != height or n_width != width:
            height, width = n_height, n_width
            grid_rows = max(3, height - 4)
            grid_cols = max(3, width)
            engine.resize(grid_rows, grid_cols)
            stdscr.clear()

        # Update simulation if not paused
        if not paused:
            engine.step()

        alive_count = engine.get_alive_count()

        # Render grid
        stdscr.erase()
        cell_attr = curses.color_pair(1) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD

        for r in range(min(grid_rows, len(engine.grid))):
            row_chars = []
            for c in range(min(grid_cols, len(engine.grid[r]))):
                row_chars.append(cell_char if engine.grid[r][c] else " ")
            safe_addstr(stdscr, r, 0, "".join(row_chars), cell_attr)

        # Render Header / Title
        header_attr = curses.color_pair(2) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        safe_addstr(stdscr, height - 3, 0, "── Conway's Game of Life ──", header_attr)
        credits_str = "Keys: [Space] Pause | [n] Step | [r] Rand | [c] Clear | [w] Wrap | [1-5] Presets | [q] Quit"
        safe_addstr(stdscr, height - 2, 0, credits_str, curses.color_pair(4) if curses.has_colors() else 0)

        # Render Status Bar
        status_bar = f"Gen: {engine.generation} | Alive: {alive_count} | Speed: {current_speed:.2f}s | Wrap: {'ON' if engine.wrap else 'OFF'} | State: {status_msg}"
        status_attr = curses.color_pair(3) | curses.A_REVERSE if curses.has_colors() else curses.A_REVERSE
        safe_addstr(stdscr, height - 1, 0, status_bar.ljust(width - 1), status_attr)

        stdscr.refresh()
        time.sleep(current_speed)

        # Key event handling
        try:
            ch = stdscr.getch()
        except curses.error:
            ch = -1

        if ch == ord('q') or ch == 27:  # 'q' or Esc
            break
        elif ch == ord(' ') or ch == ord('p'):  # Pause / Resume
            paused = not paused
            status_msg = "PAUSED" if paused else "Running"
        elif ch == ord('n') and paused:  # Single step when paused
            engine.step()
        elif ch == ord('r'):  # Randomize
            engine.seed_random(density=0.25)
            status_msg = "Randomized"
        elif ch == ord('c'):  # Clear
            engine.clear()
            status_msg = "Cleared"
        elif ch == ord('w'):  # Toggle wrap
            engine.wrap = not engine.wrap
        elif ch in (ord('f'), ord('+'), ord('=')):  # Faster
            current_speed = max(0.02, current_speed - 0.03)
        elif ch in (ord('s'), ord('-'), ord('_')):  # Slower
            current_speed = min(1.0, current_speed + 0.03)
        # Preset shortcuts
        elif ch == ord('1'):
            engine.load_preset("blinker")
            status_msg = "Preset: Blinker"
        elif ch == ord('2'):
            engine.load_preset("glider")
            status_msg = "Preset: Glider"
        elif ch == ord('3'):
            engine.load_preset("pulsar")
            status_msg = "Preset: Pulsar"
        elif ch == ord('4'):
            engine.load_preset("gosper_gun")
            status_msg = "Preset: Gosper Gun"
        elif ch == ord('5'):
            engine.load_preset("beacon")
            status_msg = "Preset: Beacon"


def run_ansi_terminal_mode(preset: str = "random", speed: float = 0.15, rows: int = 20, cols: int = 50,
                           steps: Optional[int] = None, wrap: bool = True):
    """Fallback terminal rendering using ANSI escape sequences."""
    engine = GameOfLifeEngine(rows=rows, cols=cols, wrap=wrap)
    if preset == "random" or preset not in engine.PRESETS:
        engine.seed_random(density=0.25)
    else:
        engine.load_preset(preset)

    step_count = 0
    try:
        while True:
            # Clear screen ANSI code
            sys.stdout.write("\033[H\033[J")
            sys.stdout.write(f"=== Conway's Game of Life (Terminal Mode) ===\n")
            sys.stdout.write(f"Gen: {engine.generation} | Alive: {engine.get_alive_count()} | Wrap: {'ON' if engine.wrap else 'OFF'}\n")
            sys.stdout.write("+" + "-" * cols + "+\n")

            for r in range(engine.rows):
                row_str = "".join("O" if engine.grid[r][c] else " " for c in range(engine.cols))
                sys.stdout.write(f"|{row_str}|\n")

            sys.stdout.write("+" + "-" * cols + "+\n")
            sys.stdout.write("Press Ctrl+C to exit.\n")
            sys.stdout.flush()

            step_count += 1
            if steps is not None and step_count >= steps:
                break

            time.sleep(speed)
            engine.step()

    except KeyboardInterrupt:
        print("\nExiting Conway's Game of Life.")


def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - Interactive and CLI Simulation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive Curses Mode:
    python GameOfLife.py

  Terminal (ANSI Fallback) Mode with Glider:
    python GameOfLife.py --cli --preset glider

  Run 20 simulation steps:
    python GameOfLife.py --cli --preset pulsar --steps 20
        """
    )
    parser.add_argument("--cli", action="store_true", help="Force ANSI terminal output mode (useful if curses is unavailable).")
    parser.add_argument("--preset", choices=["random", "glider", "blinker", "toad", "beacon", "pulsar", "gosper_gun"],
                        default="random", help="Initial pattern preset (default: random).")
    parser.add_argument("--speed", type=float, default=0.15, help="Simulation interval in seconds (default: 0.15).")
    parser.add_argument("--rows", type=int, default=20, help="Grid rows (CLI mode, default: 20).")
    parser.add_argument("--cols", type=int, default=50, help="Grid columns (CLI mode, default: 50).")
    parser.add_argument("--steps", type=int, default=None, help="Number of steps to execute and exit (CLI mode).")
    parser.add_argument("--no-wrap", action="store_true", help="Disable toroidal grid wrap-around.")

    args = parser.parse_args()
    wrap = not args.no_wrap

    if args.cli or not HAS_CURSES:
        if not HAS_CURSES and not args.cli:
            print("Note: 'curses' module not found. Starting in ANSI terminal mode.")
            print("To enable full screen UI on Windows, run: pip install windows-curses\n")
            time.sleep(1.0)
        run_ansi_terminal_mode(preset=args.preset, speed=args.speed, rows=args.rows, cols=args.cols,
                               steps=args.steps, wrap=wrap)
    else:
        try:
            curses.wrapper(lambda stdscr: run_curses_ui(stdscr, preset=args.preset, speed=args.speed, wrap=wrap))
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()