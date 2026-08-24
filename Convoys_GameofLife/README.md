<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
[![View My Profile](https://img.shields.io/badge/View-My_Profile-green?logo=GitHub)](https://github.com/zeal2end)

# Conway's Game of Life

<p align="center">
<img src="ConwayGif.gif" width=40% height=40% alt="Conway's Game of Life Animation">
</p>

## 🛠️ Description

A feature-rich terminal simulation of **Conway's Game of Life** — the famous cellular automaton devised by British mathematician John Horton Conway. 

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells, each of which is in one of two possible states, live or dead. Every cell interacts with its eight neighbours following Conway's four rules:
1. **Underpopulation**: Any live cell with fewer than two live neighbours dies.
2. **Survival**: Any live cell with two or three live neighbours lives on to the next generation.
3. **Overpopulation**: Any live cell with more than three live neighbours dies.
4. **Reproduction**: Any dead cell with exactly three live neighbours becomes a live cell.

---

### ✨ Features
- **Interactive Curses UI**: Real-time rendering with colors, generation counters, live cell statistics, and auto-resizing.
- **ANSI Terminal Fallback**: Runs out-of-the-box in basic terminal environments even if `curses` is not installed.
- **Built-in Pattern Presets**: Instantly load famous patterns including **Glider**, **Blinker**, **Toad**, **Beacon**, **Pulsar**, and **Gosper Glider Gun**.
- **Interactive Controls**:
  - `Space` / `p`: Pause / Resume simulation
  - `n`: Single-step forward when paused
  - `r`: Randomize grid
  - `c`: Clear grid
  - `w`: Toggle Toroidal wrap-around boundaries
  - `1`-`5`: Load preset patterns
  - `f` / `+`: Increase speed (faster)
  - `s` / `-`: Decrease speed (slower)
  - `q` / `Esc`: Quit
- **CLI Automation**: Support for flags (`--cli`, `--preset`, `--speed`, `--rows`, `--cols`, `--steps`, `--no-wrap`).

---

## ⚙️ Requirements & Installation

### Linux & macOS
Python standard library includes `curses` out of the box:
```sh
pip install -r requirements.txt
```

### Windows
On Windows, install `windows-curses` for the interactive full-screen curses UI:
```sh
pip install windows-curses
```
*(Note: If `windows-curses` is not installed, the script will automatically run in ANSI Terminal Mode!)*

---

## 🌟 How to Run

### 1. Interactive UI (Curses)
```sh
python GameOfLife.py
```

### 2. Launch with a Specific Preset
```sh
python GameOfLife.py --preset pulsar
```

### 3. Command-Line (ANSI Fallback) Mode
```sh
python GameOfLife.py --cli --preset glider --speed 0.1
```

### 4. Run for a Fixed Number of Steps
```sh
python GameOfLife.py --cli --preset gosper_gun --steps 50
```

---

## 📺 Demo
<p align="center">
<img src="demo.png" width=40% height=40% alt="Conway's Game of Life in CommandLine">
</p>

---

## 🧪 Running Automated Tests

Run the unit test suite to verify the simulation rules, oscillators, still lifes, and presets:
```sh
python -m unittest test_game_of_life.py -v
```

---

## 🤖 Authors & Contributors
- **Original Author**: [Vivek Kumar](https://github.com/zeal2end)
- **Improvements & Fixes**: Open Source Contributors