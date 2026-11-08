<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Pomodoro Timer

## 🛠️ Description

A small command-line timer that alternates focused work sessions with short breaks, and supports a longer break after every four completed focus sessions. The timer uses only Python's standard library.

## ⚙️ Languages or Frameworks Used

- Python 3
- No third-party packages required

## 🌟 How to run

From the repository root, start the default four-cycle timer (25-minute focus sessions and 5-minute breaks):

```bash
python Pomodoro_Timer/pomodoro_timer.py
```

Customize the durations and number of focus cycles (durations are in minutes):

```bash
python Pomodoro_Timer/pomodoro_timer.py --work 30 --short-break 5 --long-break 20 --cycles 4
```

Press `Ctrl+C` to stop the timer. Use `python3` instead of `python` if that is how Python 3 is invoked on your system.

## 🤖 Author

itskalpesh
