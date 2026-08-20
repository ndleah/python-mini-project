<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Exercise Timer CLI

## ??? Description

A Python CLI application designed to automate workout interval timing and repetition counting. It provides audio feedback for start, stop, and completion cues alongside a real-time countdown timer in the terminal, eliminating the need to manually reset stopwatches between sets.

### Key Features:
- **Audio Feedback**: Automatic start, stop, and completion sound alerts using Pygame mixer.
- **Live Terminal Countdown**: Real-time display of elapsed workout and rest durations.
- **Customizable Timing**: Configure exercise duration, rest interval, number of reps, and initial prep time.
- **Clean Interrupt Handling**: Safely abort anytime using `Ctrl + C`.

---

## ?? Languages or Frameworks Used

- **Python 3**
- **Click**: Command-line interface creation and option parsing.
- **Pygame**: Cross-platform audio playback.

Install the required dependencies using:
```bash
pip install -r requirements.txt
```

---

## ?? How to run

Navigate to the project folder and run the script:

```bash
python exercise_cli.py --help
```

### Examples:
- **Default workout (5 reps of 10s work, 3s rest):**
  ```bash
  python exercise_cli.py
  ```

- **Custom workout (10 reps of 30s plank, 10s rest, 5s preparation):**
  ```bash
  python exercise_cli.py -t 30 -i 10 -r 10 -p 5
  ```

### Available CLI Flags:
| Flag | Option | Default | Description |
|---|---|---|---|
| `-t` | `--time` | `10` | Exercise duration per rep (seconds) |
| `-i` | `--interval` | `3` | Rest interval between reps (seconds) |
| `-r` | `--reps` | `5` | Number of reps to perform |
| `-p` | `--prep` | `3` | Preparation countdown before first rep (seconds) |
| `-h` | `--help` | - | Display help menu and options |

To stop the workout at any time, press `CTRL + C`.

---

## ?? Author

- Original Author: [hisham-slm](https://github.com/hisham-slm)
