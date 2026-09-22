#!/usr/bin/env python3
"""
Conway's Game of Life
=====================
A full-featured simulation of Conway's cellular automaton with:
- Interactive curses UI with real-time responsive non-blocking controls
- In-place Cell Drawing / Edit Mode (cursor navigation and cell toggling)
- Non-blocking ANSI terminal mode for environments without curses (Windows/Linux/macOS)
- Universal RLE (Run Length Encoded) & Plaintext pattern importing and exporting
- Automated cycle & stability detection (Extinction, Still Life, Oscillators)
- Expanded pattern preset library (Glider, Pulsar, Gosper Gun, LWSS, Pentadecathlon, Acorn, etc.)
- Decoupled, thoroughly tested GameOfLifeEngine
"""

import collections
import os
import random
import re
import sys
import time
import argparse
from typing import List, Tuple, Optional, Set, Dict

# Optional curses import (with Windows compatibility handling)
try:
    import curses
    HAS_CURSES = True
except ImportError:
    HAS_CURSES = False

# Cross-platform non-blocking keyboard input setup for terminal mode
IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    import msvcrt
    # Enable Windows VT100 / ANSI escape sequences
    os.system("")
else:
    import select
    import termios
    import tty


def get_terminal_char_nonblocking() -> Optional[str]:
    """Read a single character from stdin without blocking, cross-platform."""
    if IS_WINDOWS:
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            # Handle special/arrow keys prefix
            if ch in (b'\x00', b'\xe0'):
                if msvcrt.kbhit():
                    msvcrt.getch()  # consume secondary code
                return None
            try:
                return ch.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                return None
        return None
    else:
        # POSIX select-based non-blocking read
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None


class GameOfLifeEngine:
    """Core simulation engine for Conway's Game of Life."""

    PRESETS: Dict[str, List[Tuple[int, int]]] = {
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
        ],
        "lwss": [
            (0, 1), (0, 4),
            (1, 0),
            (2, 0), (2, 4),
            (3, 0), (3, 1), (3, 2), (3, 3)
        ],
        "pentadecathlon": [
            (0, 1), (1, 1),
            (2, 0), (2, 2),
            (3, 1), (4, 1), (5, 1), (6, 1),
            (7, 0), (7, 2),
            (8, 1), (9, 1)
        ],
        "diehard": [
            (0, 6),
            (1, 0), (1, 1),
            (2, 1), (2, 5), (2, 6), (2, 7)
        ],
        "acorn": [
            (0, 1),
            (1, 3),
            (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)
        ]
    }

    def __init__(self, rows: int = 20, cols: int = 40, wrap: bool = True, max_history: int = 32):
        self.rows = max(3, rows)
        self.cols = max(3, cols)
        self.wrap = wrap
        self.grid = self._create_grid()
        self.generation = 0
        self.max_history = max_history
        self._history: collections.deque = collections.deque(maxlen=max_history)
        self._record_history()

    def _create_grid(self) -> List[List[bool]]:
        return [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def _grid_signature(self) -> Tuple[Tuple[int, ...], ...]:
        """Compute an immutable representation of active cell positions for cycle detection."""
        return tuple(
            tuple(c for c in range(self.cols) if self.grid[r][c])
            for r in range(self.rows)
        )

    def _record_history(self):
        """Record current grid signature in rolling history deque."""
        self._history.append(self._grid_signature())

    def sync_history(self):
        """Synchronize rolling history with current grid state (useful after direct grid manipulation)."""
        self._history.clear()
        self._record_history()

    def detect_status(self) -> Tuple[str, Optional[int]]:
        """
        Analyze recent history to detect simulation state:
        Returns:
            ("extinct", None): Grid has 0 living cells.
            ("stable", 1): Reached static still-life (period 1).
            ("oscillator", p): Periodic oscillator of period p (2 <= p <= 16).
            ("active", None): Simulation is dynamically evolving.
        """
        alive = self.get_alive_count()
        if alive == 0:
            return "extinct", None

        if len(self._history) < 2:
            return "active", None

        current_sig = self._history[-1]
        history_list = list(self._history)

        # Check for still life (same as immediately preceding generation)
        if len(history_list) >= 2 and current_sig == history_list[-2]:
            return "stable", 1

        # Check for oscillators of period p
        for p in range(2, min(17, len(history_list))):
            if current_sig == history_list[-(p + 1)]:
                return "oscillator", p

        return "active", None

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
        self._history.clear()
        self._record_history()

    def clear(self):
        """Clear all cells and reset generation count."""
        self.grid = self._create_grid()
        self.generation = 0
        self._history.clear()
        self._record_history()

    def seed_random(self, density: float = 0.25):
        """Seed the grid randomly with the given alive probability."""
        self.generation = 0
        self._history.clear()
        density = max(0.0, min(1.0, density))
        self.grid = [
            [random.random() < density for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self._record_history()

    def toggle_cell(self, r: int, c: int) -> bool:
        """Toggle cell alive/dead state at (r, c) if within bounds."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = not self.grid[r][c]
            self._history.clear()
            self._record_history()
            return self.grid[r][c]
        return False

    def set_cell(self, r: int, c: int, state: bool):
        """Explicitly set cell state at (r, c)."""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.grid[r][c] = bool(state)
            self._history.clear()
            self._record_history()

    def load_preset(self, name: str, start_r: Optional[int] = None, start_c: Optional[int] = None) -> bool:
        """Load a predefined pattern into the grid with proper bounding box centering."""
        pattern = self.PRESETS.get(name.lower())
        if not pattern:
            return False

        min_pr = min(r for r, _ in pattern)
        max_pr = max(r for r, _ in pattern)
        min_pc = min(c for _, c in pattern)
        max_pc = max(c for _, c in pattern)

        pattern_h = max_pr - min_pr + 1
        pattern_w = max_pc - min_pc + 1

        if start_r is None:
            start_r = max(0, (self.rows - pattern_h) // 2)
        if start_c is None:
            start_c = max(0, (self.cols - pattern_w) // 2)

        self.clear()
        for r, c in pattern:
            target_r = start_r + (r - min_pr)
            target_c = start_c + (c - min_pc)
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r][target_c] = True

        self._history.clear()
        self._record_history()
        return True

    def load_rle(self, rle_string: str, start_r: Optional[int] = None, start_c: Optional[int] = None) -> bool:
        """
        Parse and load a standard Run Length Encoded (RLE) string.
        Supports standard tags: 'b' (dead), 'o' (alive), '$' (newline), '!' (end of pattern).
        """
        lines = [line.strip() for line in rle_string.strip().splitlines() if line.strip()]
        if not lines:
            return False

        # Filter out comments and header lines
        content_lines = []
        for line in lines:
            if line.startswith("#"):
                continue
            if re.match(r"^[xy]\s*=", line, re.IGNORECASE):
                continue
            content_lines.append(line)

        encoded_data = "".join(content_lines)
        if not encoded_data:
            return False

        cells = []
        cur_r = 0
        cur_c = 0
        tokens = re.findall(r"(\d*)([bo\$!])", encoded_data)

        for count_str, tag in tokens:
            count = int(count_str) if count_str else 1
            if tag == "b":  # Dead cells
                cur_c += count
            elif tag == "o":  # Alive cells
                for _ in range(count):
                    cells.append((cur_r, cur_c))
                    cur_c += 1
            elif tag == "$":  # Row break
                cur_r += count
                cur_c = 0
            elif tag == "!":  # End of pattern
                break

        if not cells:
            return False

        min_pr = min(r for r, _ in cells)
        max_pr = max(r for r, _ in cells)
        min_pc = min(c for _, c in cells)
        max_pc = max(c for _, c in cells)

        pattern_h = max_pr - min_pr + 1
        pattern_w = max_pc - min_pc + 1

        if start_r is None:
            start_r = max(0, (self.rows - pattern_h) // 2)
        if start_c is None:
            start_c = max(0, (self.cols - pattern_w) // 2)

        self.clear()
        for r, c in cells:
            target_r = start_r + (r - min_pr)
            target_c = start_c + (c - min_pc)
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r][target_c] = True

        self._history.clear()
        self._record_history()
        return True

    def load_plaintext(self, cells_string: str, start_r: Optional[int] = None, start_c: Optional[int] = None) -> bool:
        """Parse and load a standard Plaintext (.cells) format string."""
        raw_lines = cells_string.strip().splitlines()
        cells = []
        r_offset = 0

        for line in raw_lines:
            line = line.strip()
            if not line or line.startswith("!"):
                continue
            for c_idx, char in enumerate(line):
                if char in ("O", "o", "*", "#"):
                    cells.append((r_offset, c_idx))
            r_offset += 1

        if not cells:
            return False

        min_pr = min(r for r, _ in cells)
        max_pr = max(r for r, _ in cells)
        min_pc = min(c for _, c in cells)
        max_pc = max(c for _, c in cells)

        pattern_h = max_pr - min_pr + 1
        pattern_w = max_pc - min_pc + 1

        if start_r is None:
            start_r = max(0, (self.rows - pattern_h) // 2)
        if start_c is None:
            start_c = max(0, (self.cols - pattern_w) // 2)

        self.clear()
        for r, c in cells:
            target_r = start_r + (r - min_pr)
            target_c = start_c + (c - min_pc)
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r][target_c] = True

        self._history.clear()
        self._record_history()
        return True

    def export_rle(self, name: str = "ConwayPattern") -> str:
        """Export current grid state to standard Run Length Encoded (RLE) format."""
        alive_cells = [
            (r, c) for r in range(self.rows) for c in range(self.cols) if self.grid[r][c]
        ]
        if not alive_cells:
            return f"#N {name}\nx = 0, y = 0, rule = B3/S23\n!"

        min_r = min(r for r, _ in alive_cells)
        max_r = max(r for r, _ in alive_cells)
        min_c = min(c for _, c in alive_cells)
        max_c = max(c for _, c in alive_cells)

        width = max_c - min_c + 1
        height = max_r - min_r + 1

        lines = [f"#N {name}", f"x = {width}, y = {height}, rule = B3/S23"]
        rle_chunks = []

        consecutive_dollars = 0
        for r in range(min_r, max_r + 1):
            row_items = []
            cur_tag = None
            cur_count = 0
            for c in range(min_c, max_c + 1):
                tag = "o" if self.grid[r][c] else "b"
                if tag == cur_tag:
                    cur_count += 1
                else:
                    if cur_tag is not None:
                        # Omit trailing dead cells at end of line
                        row_items.append((cur_count, cur_tag))
                    cur_tag = tag
                    cur_count = 1
            if cur_tag is not None:
                row_items.append((cur_count, cur_tag))

            # Strip trailing dead cells 'b' from line
            while row_items and row_items[-1][1] == "b":
                row_items.pop()

            if not row_items:
                consecutive_dollars += 1
            else:
                if consecutive_dollars > 0:
                    rle_chunks.append(f"{consecutive_dollars}$" if consecutive_dollars > 1 else "$")
                    consecutive_dollars = 0
                for count, tag in row_items:
                    rle_chunks.append(f"{count}{tag}" if count > 1 else tag)
                consecutive_dollars = 1

        rle_chunks.append("!")
        encoded = "".join(rle_chunks)

        # Split into lines max 70 chars per standard RLE convention
        for i in range(0, len(encoded), 70):
            lines.append(encoded[i:i + 70])

        return "\n".join(lines)

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
        self._record_history()
        return self.generation, alive_count

    def get_alive_count(self) -> int:
        """Count total alive cells currently on the grid."""
        return sum(row.count(True) for row in self.grid)


def safe_addstr(window, y: int, x: int, text: str, attr: int = 0):
    """Safely draw string avoiding curses boundary overflow exceptions."""
    max_y, max_x = window.getmaxyx()
    if y < 0 or y >= max_y or x < 0 or x >= max_x:
        return
    available_len = max_x - x
    if y == max_y - 1:
        available_len = max(0, available_len - 1)
    
    truncated_text = text[:available_len]
    try:
        window.addstr(y, x, truncated_text, attr)
    except curses.error:
        pass


def run_curses_ui(stdscr, preset: str = "random", speed: float = 0.15, wrap: bool = True,
                  rle_content: Optional[str] = None, cells_content: Optional[str] = None,
                  density: float = 0.25):
    """Run interactive curses interface with responsive timeout and interactive edit mode."""
    curses.curs_set(0)
    stdscr.clear()

    # Color pairs setup
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)     # Living cells
        curses.init_pair(2, curses.COLOR_GREEN, -1)    # Title & controls
        curses.init_pair(3, curses.COLOR_YELLOW, -1)   # Status bar
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)  # Presets / shortcuts
        curses.init_pair(5, curses.COLOR_RED, -1)      # Edit mode / cursor

    height, width = stdscr.getmaxyx()
    grid_rows = max(3, height - 4)
    grid_cols = max(3, width)

    engine = GameOfLifeEngine(rows=grid_rows, cols=grid_cols, wrap=wrap)

    if rle_content:
        engine.load_rle(rle_content)
    elif cells_content:
        engine.load_plaintext(cells_content)
    elif preset == "random" or preset not in engine.PRESETS:
        engine.seed_random(density=density)
    else:
        engine.load_preset(preset)

    paused = False
    edit_mode = False
    cursor_r = grid_rows // 2
    cursor_c = grid_cols // 2
    current_speed = speed
    status_msg = "Running"
    cell_char = "O"

    preset_keys = {
        ord('1'): "blinker",
        ord('2'): "toad",
        ord('3'): "beacon",
        ord('4'): "glider",
        ord('5'): "pulsar",
        ord('6'): "gosper_gun",
        ord('7'): "lwss",
        ord('8'): "pentadecathlon",
        ord('9'): "acorn",
    }

    while True:
        # Check window resize
        n_height, n_width = stdscr.getmaxyx()
        if n_height != height or n_width != width:
            height, width = n_height, n_width
            grid_rows = max(3, height - 4)
            grid_cols = max(3, width)
            engine.resize(grid_rows, grid_cols)
            cursor_r = min(cursor_r, grid_rows - 1)
            cursor_c = min(cursor_c, grid_cols - 1)
            stdscr.clear()

        # Update simulation if not paused and not in edit mode
        if not paused and not edit_mode:
            engine.step()

        alive_count = engine.get_alive_count()
        state_kind, period = engine.detect_status()
        if state_kind == "extinct":
            status_msg = "Extinct (0 Alive)"
        elif state_kind == "stable":
            status_msg = "Still Life (Period 1)"
        elif state_kind == "oscillator":
            status_msg = f"Oscillator (P={period})"
        elif edit_mode:
            status_msg = "EDIT MODE"
        elif paused:
            status_msg = "PAUSED"
        else:
            status_msg = "Running"

        # Render grid
        stdscr.erase()
        cell_attr = curses.color_pair(1) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD

        for r in range(min(grid_rows, len(engine.grid))):
            row_chars = []
            for c in range(min(grid_cols, len(engine.grid[r]))):
                if edit_mode and r == cursor_r and c == cursor_c:
                    row_chars.append("X" if engine.grid[r][c] else "+")
                else:
                    row_chars.append(cell_char if engine.grid[r][c] else " ")
            safe_addstr(stdscr, r, 0, "".join(row_chars), cell_attr)

        # Highlight cursor cell in Edit Mode
        if edit_mode and 0 <= cursor_r < grid_rows and 0 <= cursor_c < grid_cols:
            cur_char = "X" if engine.grid[cursor_r][cursor_c] else "+"
            cursor_attr = curses.color_pair(5) | curses.A_REVERSE | curses.A_BOLD if curses.has_colors() else curses.A_REVERSE
            safe_addstr(stdscr, cursor_r, cursor_c, cur_char, cursor_attr)

        # Render Header / Title
        header_attr = curses.color_pair(2) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        safe_addstr(stdscr, height - 3, 0, "── Conway's Game of Life ──", header_attr)

        if edit_mode:
            help_str = "EDIT: [Arrows/WASD] Move | [Space/Enter] Toggle | [c] Clear | [e] Exit Edit"
            help_attr = curses.color_pair(5) | curses.A_BOLD if curses.has_colors() else curses.A_BOLD
        else:
            help_str = "[Space] Pause | [e] Edit | [n] Step | [r] Rand | [c] Clear | [w] Wrap | [1-9] Presets | [q] Quit"
            help_attr = curses.color_pair(4) if curses.has_colors() else 0
        safe_addstr(stdscr, height - 2, 0, help_str, help_attr)

        # Render Status Bar
        status_bar = f"Gen: {engine.generation} | Alive: {alive_count} | Spd: {current_speed:.2f}s | Wrap: {'ON' if engine.wrap else 'OFF'} | {status_msg}"
        status_attr = curses.color_pair(3) | curses.A_REVERSE if curses.has_colors() else curses.A_REVERSE
        safe_addstr(stdscr, height - 1, 0, status_bar.ljust(width - 1), status_attr)

        stdscr.refresh()

        # Non-blocking timeout-based key wait (responsive input without sleeping thread)
        if paused or edit_mode:
            stdscr.timeout(100)  # Responsively poll input without consuming 100% CPU
        else:
            timeout_ms = max(10, int(current_speed * 1000))
            stdscr.timeout(timeout_ms)

        try:
            ch = stdscr.getch()
        except curses.error:
            ch = -1

        if ch == -1:
            continue

        # Common exits
        if ch == ord('q') or ch == 27:  # 'q' or Esc
            break

        # Toggle Edit Mode
        if ch in (ord('e'), ord('E')):
            edit_mode = not edit_mode
            if edit_mode:
                paused = True
            continue

        if edit_mode:
            # Edit mode navigation & toggling
            if ch in (curses.KEY_UP, ord('w'), ord('W'), ord('k'), ord('K')):
                cursor_r = max(0, cursor_r - 1)
            elif ch in (curses.KEY_DOWN, ord('s'), ord('S'), ord('j'), ord('J')):
                cursor_r = min(grid_rows - 1, cursor_r + 1)
            elif ch in (curses.KEY_LEFT, ord('a'), ord('A'), ord('h'), ord('H')):
                cursor_c = max(0, cursor_c - 1)
            elif ch in (curses.KEY_RIGHT, ord('d'), ord('D'), ord('l'), ord('L')):
                cursor_c = min(grid_cols - 1, cursor_c + 1)
            elif ch in (ord(' '), 10, 13, curses.KEY_ENTER):  # Space or Enter toggles
                engine.toggle_cell(cursor_r, cursor_c)
            elif ch in (ord('c'), ord('C')):
                engine.clear()
            elif ch in (ord('r'), ord('R')):
                engine.seed_random(density=density)
            continue

        # Simulation mode key bindings
        if ch in (ord(' '), ord('p'), ord('P')):  # Pause / Resume
            paused = not paused
        elif ch in (ord('n'), ord('N')):  # Single step forward
            paused = True
            engine.step()
        elif ch in (ord('r'), ord('R')):  # Randomize
            engine.seed_random(density=density)
        elif ch in (ord('c'), ord('C')):  # Clear
            engine.clear()
        elif ch in (ord('w'), ord('W')):  # Toggle wrap
            engine.wrap = not engine.wrap
        elif ch in (ord('f'), ord('+'), ord('=')):  # Faster
            current_speed = max(0.02, current_speed - 0.03)
        elif ch in (ord('s'), ord('-'), ord('_')):  # Slower
            current_speed = min(1.0, current_speed + 0.03)
        elif ch in preset_keys:
            p_name = preset_keys[ch]
            engine.load_preset(p_name)


def run_ansi_terminal_mode(preset: str = "random", speed: float = 0.15, rows: int = 20, cols: int = 50,
                           steps: Optional[int] = None, wrap: bool = True,
                           rle_content: Optional[str] = None, cells_content: Optional[str] = None,
                           density: float = 0.25, alive_char: str = "O", dead_char: str = " "):
    """
    Terminal rendering using ANSI escape sequences with cross-platform
    non-blocking interactive keyboard controls (Pause, Step, Speed, Clear, Randomize, Quit).
    """
    engine = GameOfLifeEngine(rows=rows, cols=cols, wrap=wrap)

    if rle_content:
        engine.load_rle(rle_content)
    elif cells_content:
        engine.load_plaintext(cells_content)
    elif preset == "random" or preset not in engine.PRESETS:
        engine.seed_random(density=density)
    else:
        engine.load_preset(preset)

    step_count = 0
    paused = False
    current_speed = speed
    status_msg = "Running"

    preset_keys = {
        '1': "blinker",
        '2': "toad",
        '3': "beacon",
        '4': "glider",
        '5': "pulsar",
        '6': "gosper_gun",
        '7': "lwss",
        '8': "pentadecathlon",
        '9': "acorn",
    }

    try:
        while True:
            # Poll non-blocking keyboard input
            key = get_terminal_char_nonblocking()
            if key:
                if key.lower() == 'q':
                    print("\nExiting Conway's Game of Life.")
                    break
                elif key in (' ', 'p', 'P'):
                    paused = not paused
                elif key in ('n', 'N'):
                    paused = True
                    engine.step()
                    step_count += 1
                elif key in ('r', 'R'):
                    engine.seed_random(density=density)
                elif key in ('c', 'C'):
                    engine.clear()
                elif key in ('w', 'W'):
                    engine.wrap = not engine.wrap
                elif key in ('+', 'f', '='):
                    current_speed = max(0.02, current_speed - 0.03)
                elif key in ('-', 's', '_'):
                    current_speed = min(1.0, current_speed + 0.03)
                elif key in preset_keys:
                    engine.load_preset(preset_keys[key])

            alive_count = engine.get_alive_count()
            state_kind, period = engine.detect_status()
            if state_kind == "extinct":
                status_msg = "Extinct (0 Alive)"
            elif state_kind == "stable":
                status_msg = "Still Life (Period 1)"
            elif state_kind == "oscillator":
                status_msg = f"Oscillator (Period {period})"
            elif paused:
                status_msg = "PAUSED"
            else:
                status_msg = "Running"

            # Render frame using ANSI clear sequence
            sys.stdout.write("\033[H\033[J")
            sys.stdout.write("=== Conway's Game of Life (Terminal Mode) ===\n")
            sys.stdout.write(f"Gen: {engine.generation} | Alive: {alive_count} | Speed: {current_speed:.2f}s | Wrap: {'ON' if engine.wrap else 'OFF'} | {status_msg}\n")
            sys.stdout.write("+" + "-" * cols + "+\n")

            for r in range(engine.rows):
                row_str = "".join(alive_char if engine.grid[r][c] else dead_char for c in range(engine.cols))
                sys.stdout.write(f"|{row_str}|\n")

            sys.stdout.write("+" + "-" * cols + "+\n")
            sys.stdout.write("Controls: [Space] Pause | [n] Step | [r] Rand | [c] Clear | [w] Wrap | [1-9] Presets | [q] Quit\n")
            sys.stdout.flush()

            # Check steps termination condition
            if steps is not None and step_count >= steps:
                break

            # Sleep slice for responsive non-blocking input
            sleep_slices = max(1, int(current_speed / 0.05))
            for _ in range(sleep_slices):
                time.sleep(current_speed / sleep_slices)
                sub_key = get_terminal_char_nonblocking()
                if sub_key:
                    if sub_key.lower() == 'q':
                        print("\nExiting Conway's Game of Life.")
                        return
                    elif sub_key in (' ', 'p', 'P'):
                        paused = not paused
                        break
                    elif sub_key in ('n', 'N'):
                        paused = True
                        engine.step()
                        step_count += 1
                        break
                    elif sub_key in ('r', 'R'):
                        engine.seed_random(density=density)
                        break
                    elif sub_key in ('c', 'C'):
                        engine.clear()
                        break
                    elif sub_key in ('w', 'W'):
                        engine.wrap = not engine.wrap
                        break
                    elif sub_key in ('+', 'f', '='):
                        current_speed = max(0.02, current_speed - 0.03)
                    elif sub_key in ('-', 's', '_'):
                        current_speed = min(1.0, current_speed + 0.03)
                    elif sub_key in preset_keys:
                        engine.load_preset(preset_keys[sub_key])
                        break

            if not paused:
                engine.step()
                step_count += 1

    except KeyboardInterrupt:
        print("\nExiting Conway's Game of Life.")


def main():
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - Interactive Curses & CLI Simulation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive Full-screen Mode (Curses):
    python GameOfLife.py

  Interactive Edit Mode:
    python GameOfLife.py  (then press 'e' to draw cells using Arrow keys / Space)

  Load a Preset Pattern:
    python GameOfLife.py --preset pulsar

  Load from standard RLE string:
    python GameOfLife.py --rle "3o$o$bo!"

  Load from RLE or Plaintext file:
    python GameOfLife.py --file patterns/glider_gun.rle

  Terminal (ANSI Fallback) Mode with Custom Speed:
    python GameOfLife.py --cli --preset glider --speed 0.1

  Automated Fixed Step Execution:
    python GameOfLife.py --cli --preset gosper_gun --steps 50 --export
        """
    )
    parser.add_argument("--cli", action="store_true", help="Force ANSI terminal output mode (runs out-of-the-box everywhere).")
    parser.add_argument("--preset", choices=[
        "random", "glider", "blinker", "toad", "beacon", "pulsar", "gosper_gun",
        "lwss", "pentadecathlon", "diehard", "acorn"
    ], default="random", help="Initial pattern preset (default: random).")
    parser.add_argument("--rle", type=str, default=None, help="Inline Run Length Encoded (RLE) pattern string to load.")
    parser.add_argument("--file", type=str, default=None, help="Path to .rle or .cells pattern file to load.")
    parser.add_argument("--density", type=float, default=0.25, help="Random grid density between 0.0 and 1.0 (default: 0.25).")
    parser.add_argument("--speed", type=float, default=0.15, help="Simulation interval in seconds (default: 0.15).")
    parser.add_argument("--rows", type=int, default=20, help="Grid rows (CLI mode, default: 20).")
    parser.add_argument("--cols", type=int, default=50, help="Grid columns (CLI mode, default: 50).")
    parser.add_argument("--steps", type=int, default=None, help="Number of steps to execute and exit (CLI mode).")
    parser.add_argument("--no-wrap", action="store_true", help="Disable toroidal grid wrap-around.")
    parser.add_argument("--alive-char", type=str, default="O", help="Character to represent living cells in CLI mode (default: 'O').")
    parser.add_argument("--dead-char", type=str, default=" ", help="Character to represent dead cells in CLI mode (default: ' ').")
    parser.add_argument("--export", action="store_true", help="Export final grid state to RLE format on exit.")

    args = parser.parse_args()
    wrap = not args.no_wrap

    rle_content = args.rle
    cells_content = None

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: Pattern file '{args.file}' not found.")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if args.file.lower().endswith(".cells"):
                cells_content = content
            else:
                rle_content = content

    if args.cli or not HAS_CURSES:
        if not HAS_CURSES and not args.cli:
            print("Note: 'curses' module not found. Starting in ANSI terminal mode.")
            print("To enable full screen UI on Windows, run: pip install windows-curses\n")
            time.sleep(0.8)
        run_ansi_terminal_mode(preset=args.preset, speed=args.speed, rows=args.rows, cols=args.cols,
                               steps=args.steps, wrap=wrap, rle_content=rle_content,
                               cells_content=cells_content, density=args.density,
                               alive_char=args.alive_char[:1] if args.alive_char else "O",
                               dead_char=args.dead_char[:1] if args.dead_char else " ")
    else:
        try:
            curses.wrapper(lambda stdscr: run_curses_ui(stdscr, preset=args.preset, speed=args.speed, wrap=wrap,
                                                        rle_content=rle_content, cells_content=cells_content,
                                                        density=args.density))
        except KeyboardInterrupt:
            pass

    if args.export:
        engine = GameOfLifeEngine(rows=args.rows, cols=args.cols, wrap=wrap)
        if rle_content:
            engine.load_rle(rle_content)
        elif cells_content:
            engine.load_plaintext(cells_content)
        elif args.preset != "random":
            engine.load_preset(args.preset)
        print("\n--- Exported Pattern (RLE) ---")
        print(engine.export_rle())


if __name__ == "__main__":
    main()