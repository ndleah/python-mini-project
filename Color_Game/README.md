# Color Game

A fun and interactive Python Tkinter GUI game based on the Stroop Effect. The player must enter the font color of the displayed word, rather than the text of the word itself, within a 30-second time limit.

## Features
- **Stroop Effect Challenge**: Tests cognitive processing and reaction time by presenting mismatched word names and colors.
- **Timer & Real-Time Scoring**: 30-second countdown with immediate score updates.
- **High Score Persistence**: Automatically tracks and saves the highest score in `highest_score.txt`.
- **Game Restart & Replay**: Easy restart mechanism to play multiple rounds.
- **Cross-Platform Compatibility**: Robust path resolution and safe icon handling across platforms.

## Prerequisites
- Python 3.x
- Tkinter (included by default in standard Python installations)

## How to Run
1. Navigate to the `Color_Game` directory:
   ```bash
   cd Color_Game
   ```
2. Run the script:
   ```bash
   python main.py
   ```

## Rules / Gameplay
- Press `Enter` to start the game.
- Type the **color of the text** (e.g. if the word "BLUE" is shown in red font, type `red`) into the input box and press `Enter`.
- Score as many points as possible before the 30-second timer expires!