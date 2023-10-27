
# Voice-Controlled Desktop Assistant

A simple voice-controlled desktop assistant in Python that can perform various tasks based on user commands.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Python script is a voice-controlled desktop assistant that utilizes the `pyttsx3` library for text-to-speech, `speech_recognition` for voice input, and other libraries to perform various tasks. The assistant can perform actions like searching Wikipedia, opening web pages, providing the current time, and launching applications.

## Features

- Greet the user based on the time of day.
- Accept voice commands and convert them to text.
- Search and read summaries from Wikipedia.
- Open YouTube videos based on user input.
- Open Google, Stack Overflow, or LeetCode in a web browser.
- Provide the current time.
- Open Visual Studio Code.

## Requirements

Before running the code, make sure you have the following Python libraries installed:

- `pyttsx3`
- `datetime`
- `speech_recognition`
- `wikipedia`
- `webbrowser`
- `pyautogui`
- `time`
- `os`
- `pywhatkit`
- `spotipy` (and Spotify authentication, if you plan to use it)

You can install these libraries using the following command:

```shell
pip install pyttsx3 datetime speech_recognition wikipedia webbrowser pyautogui pywhatkit spotipy
```

Please note that you might need to set up authentication for the Spotify functionality if you intend to use it.

## Usage

1. Run the Python script using a compatible Python interpreter.

```shell
python your_script.py
```

2. The assistant will greet you based on the time of day and wait for your voice command.

3. Speak your command clearly, and the assistant will attempt to perform the requested task.

4. The assistant can perform tasks such as searching Wikipedia, opening web pages, providing the current time, and opening Visual Studio Code.

5. To stop and exit the assistant, simply say "stop and exit."



---


