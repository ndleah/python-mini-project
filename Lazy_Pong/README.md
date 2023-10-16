![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Pong Game in Python

## 🌟 Introduction
This is a simple implementation of the classic Pong game in Python using the Pygame library. In this game, two players control paddles, trying to bounce a ball back and forth. The goal is to score points by getting the ball past the opponent's paddle.

Based on the previous version of [Ben Sicat](https://github.com/Ben-Sicat)

## 📝 Prerequisites
Before running the game, make sure you have [Python](https://www.python.org/downloads/)  to run this script, and also [PyGame](https://www.pygame.org/download.shtml). You can install Pygame using pip:

```bash
pip install pygame
```
## 🎮 How to Play

- Run the script with Python
- The game window will appear with two paddles and a ball in the middle.
- Use the arrow keys to control your paddle (Player 1) up and down.
- The CPU controls the other paddle (Player 2).
- The game starts when you press any arrow key. The ball will start moving in a random direction.
- The goal is to bounce the ball past your opponent's paddle and score points.
- The game continues until one player reaches the specified maximum score.
- If you win, your name will be displayed as the winner.

## ⚙️ Configuration
You can configure the game by modifying the script's parameters, such as screen width, screen height, player name, color, frames per second (fps), and maximum score.

```bash
python pong.py [-h] [-dw WIDTH] [-dh HEIGHT] [-n NAME] [-c COLOR] [--fps FPS] [--max_score MAX_SCORE]
options:
  -h, --help            		Show help message and exit
  -dw WIDTH, --width WIDTH		Width of the display (dflt 320)
  -dh HEIGHT, --height HEIGHT	Height of the display (dflt 240)
  -n NAME, --name NAME  		Player name
  -c COLOR, --color COLOR	  	Game color (dflt light grey)
  --fps FPS             		Framerate (dflt 120)
  --max_score MAX_SCORE         Max score to win (dflt 10)

```

## Color Options
You can change the color of the game by specifying a color from the below list of available colors: 
``` python
rgb_colors = {
		"red": (255, 0, 0),
		"green": (0, 255, 0),
		"blue": (0, 0, 255),
		"yellow": (255, 255, 0),
		"purple": (128, 0, 128),
		"orange": (255, 165, 0),
		"pink": (255, 192, 203),
		"cyan": (0, 255, 255),
		"lime": (0, 255, 0),
		"teal": (0, 128, 128),
		"navy": (0, 0, 128),
		"maroon": (128, 0, 0),
		"olive": (128, 128, 0),
		"brown": (165, 42, 42),
		"gray": (128, 128, 128),
		"black": (0, 0, 0),
		"white": (255, 255, 255),
		"silver": (192, 192, 192),
		"gold": (255, 215, 0),
		"violet": (238, 130, 238),
		"indigo": (75, 0, 130),
		"turquoise": (64, 224, 208),
		"lavender": (230, 230, 250),
		"crimson": (220, 20, 60),
		"coral": (255, 127, 80),
		"skyblue": (135, 206, 235),
		"magenta": (255, 0, 255),
		"chartreuse": (127, 255, 0),
		"sienna": (160, 82, 45),
		"plum": (221, 160, 221),
		"khaki": (240, 230, 140),
		"darkgreen": (0, 100, 0),
		"deepskyblue": (0, 191, 255),
		"limegreen": (50, 205, 50),
		"tomato": (255, 99, 71),
		"salmon": (250, 128, 114),
		"goldrod": (218, 165, 32),
		"darkorchid": (153, 50, 204),
		"peru": (205, 133, 63),
		"orchid": (218, 112, 214),
		"royalblue": (65, 105, 225),
		"indianred": (205, 92, 92),
		"yellowgreen": (154, 205, 50),
		"lightgrey" : (200, 200, 200)
}
```
The default is **lightgrey** You can choose from colors like red, green, blue, yellow, and more.

## 📺 Demo

![demo_pong](https://github.com/dar8900/python-mini-project/assets/37539290/77528c65-900f-4d8c-979e-7fedb780f988)

## 😄 Enjoy the Game!
Have fun playing this simple Pong game. Feel free to customize it and make it your own. If you encounter any issues, please refer to the script's comments and logs for troubleshooting.

## 🤖  Author
[dar8900](https://github.com/dar8900)


