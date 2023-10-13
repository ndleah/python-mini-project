from time import sleep
import os
import pygame
import sys
import random
import argparse
import logging

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

log_file = "pong_log.log"

if os.path.exists(os.path.abspath(log_file)):
	os.remove(os.path.abspath(log_file))

# Configure main logger
pong_log = logging.getLogger("Pong logger")
pong_log.setLevel(logging.DEBUG)

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Imposta il livello a INFO o altro a tuo piacere

# Configure file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Set format
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handler to logger
pong_log.addHandler(console_handler)
pong_log.addHandler(file_handler)

def get_random(limit: int):
	num_rand = random.randint(-limit, limit)
	while num_rand == 0:
		num_rand = random.randint(-limit, limit)
	return num_rand


class Ball():
	def __init__(self,
				 center_x: int,
				 center_y: int,
				 radius: int,
				 color: tuple,
				 display_width: int,
				 display_high: int,
				 speed_x: int = 0,
				 speed_y: int = 0,) -> None:

		self.center_x = center_x
		self.center_y = center_y
		self.radius = radius
		self.speed_x = speed_x
		self.speed_y = speed_y
		self.color = color
		self.display_width = display_width
		self.display_high = display_high

	def update_pos(self) -> None:
		if self.center_y - self.radius <= 0 or self.center_y + self.radius >= self.display_high:
			self.invert_move(invert_y=True)
		if self.speed_x != 0:
			self.center_x += self.speed_x
		if self.speed_y != 0:
			self.center_y += self.speed_y

	def set_speed(self, speed_x: int | float, speed_y: int | float) -> None:
		if speed_x != 0:
			if self.speed_x < 0:
				self.speed_x = -speed_x
			else:
				self.speed_x = speed_x
		if speed_y != 0:
			if self.speed_y < 0:
				self.speed_y = -speed_y
			else:
				self.speed_y = speed_y

	def invert_move(self, invert_x=False, invert_y=False):
		if invert_x:
			self.speed_x *= -1
		if invert_y:
			self.speed_y *= -1

	def get_speed(self) -> tuple:
		return (self.speed_x, self.speed_y)

	def draw(self, display: pygame.Surface) -> None:
		self.surface = display
		pygame.draw.circle(self.surface, self.color,
						   (self.center_x, self.center_y), self.radius)

	def reset(self) -> None:
		self.speed_x = 0
		self.speed_y = 0
		self.center_x = self.display_width / 2
		self.center_y = self.display_high / 2
		self.draw(self.surface)

	def get_borders(self) -> dict:
		return {
			'left': self.center_x - self.radius,
			'right': self.center_x + self.radius,
			'top': self.center_y - self.radius,
			'bott': self.center_y + self.radius,
			'center_x': self.center_x,
			'center_y': self.center_y
		}


class Gamer:
	def __init__(self, top_x: int,
				 top_y: int,
				 width: int,
				 high: int,
				 color: tuple,
				 player_name : str,
				 display_width: int,
				 display_high: int) -> None:
		self.init_top_x = top_x
		self.init_top_y = top_y
		self.width = width
		self.high = high
		self.color = color
		self.rect = pygame.Rect(top_x, top_y, width, high)
		self.speed_y = 0
		self.disp_w = display_width
		self.disp_h = display_high
		self.name = player_name

	def draw(self, display: pygame.Surface) -> None:
		pygame.draw.rect(display, self.color, self.rect)

	def update_pos(self) -> None:
		if self.speed_y != 0:
			self.rect.y += self.speed_y
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= self.disp_h:
			self.rect.bottom = self.disp_h

	def set_speed(self, speed_y: int | float) -> None:
		if speed_y == 0:
			self.speed_y = 0
		else:
			self.speed_y += speed_y

	def get_speed(self):
		return self.speed_y

	def reset(self) -> None:
		self.rect.x = self.init_top_x
		self.rect.y = self.init_top_y

	def get_borders(self) -> dict:
		return {
			'top': self.rect.top,
			'right': self.rect.right,
			'bott': self.rect.bottom,
			'left': self.rect.left,
			'center_x': self.rect.centerx,
			'center_y': self.rect.centery
		}


class GameField:
	def __init__(self, display_w: int, display_h: int, bg_color: str, line_color: tuple, caption: str) -> None:
		self.disp_w = display_w
		self.disp_h = display_h
		self.screen = pygame.display.set_mode((display_w, display_h))
		self.bg_color = pygame.Color(bg_color)
		self.caption = caption
		self.line_color = line_color
		pygame.display.set_caption(caption)

	def get_screen(self) -> pygame.Surface:
		return self.screen

	def fill_screen(self):
		self.screen.fill(self.bg_color)

	def draw_borders(self):
		pygame.draw.aaline(self.screen, self.line_color,
						   (self.disp_w / 2, 0), (self.disp_w / 2, self.disp_h))


class PongGame:
	def __init__(self, game_field: GameField,
				 ball: Ball,
				 player: Gamer,
				 computer: Gamer,
				 max_score: int = 100,
				 fps: int = 120) -> None:
		self._period = 1 / fps
		self._max_ball_time_4_travel = 3
		self._max_gamer_time_4_travel = 2
		self._pong_pygame = pygame
		self._game_field = game_field
		self._ball = ball
		self._player = player
		self._computer = computer
		self._pong_pygame.init()
		self._clock = self._pong_pygame.time.Clock()
		self._stat = {"player_score": 0, "cpu_score": 0,
					   "last_diff": 0, "level": 1, "max_score": max_score}
		self._fps = fps
		self._BALL_SPEED_X_DFLT = (self._game_field.disp_w) / (self._max_ball_time_4_travel * self._fps)
		self._BALL_SPEED_Y_DFLT = (self._game_field.disp_h) / (self._max_ball_time_4_travel * self._fps)
		self._CPU_SPEED_DFLT = (self._game_field.disp_h) / (self._max_gamer_time_4_travel * self._fps)
		self._cpu_speed_increment = 1
		self._ball_speed_increment = 0.5
		self._player_speed = (self._game_field.disp_h) / (self._max_gamer_time_4_travel * self._fps)
		self._cpu_speed = self._CPU_SPEED_DFLT

	def _reset_game(self):
		self._update_game_speed()
		self._ball.reset()
		self._player.reset()
		self._computer.reset()

	def _check_collision(self):
		ball_coord = self._ball.get_borders()
		if ball_coord['left'] <= self._computer.get_borders()['left']:
			pong_log.debug("Player score +1")
			self._stat['player_score'] += 1
			self._reset_game()

		if ball_coord['right'] >= self._player.get_borders()['right']:
			pong_log.debug("CPU score +1")
			self._stat['cpu_score'] += 1
			self._reset_game()

		if ball_coord['right'] > self._game_field.disp_w / 2 and ball_coord['right'] >= self._player.get_borders()['left']:
			if ball_coord['top'] <= self._player.get_borders()['bott'] and ball_coord['bott'] >= self._player.get_borders()['top']:
				self._ball.invert_move(invert_x=True)

		if ball_coord['left'] < self._game_field.disp_w / 2 and ball_coord['left'] <= self._computer.get_borders()['right']:
			if ball_coord['top'] <= self._computer.get_borders()['bott'] and ball_coord['bott'] >= self._computer.get_borders()['top']:
				self._ball.invert_move(invert_x=True)

	# Update game speed after a reset due to cpu error
	def _update_game_speed(self):
		score_diff = self._stat['player_score'] - self._stat['cpu_score']
		if score_diff > 0 and score_diff > self._stat['last_diff']:
			self._ball.set_speed(abs(self._ball.get_speed()[
								 0]) + self._cpu_speed_increment, abs(self._ball.get_speed()[1]) + self._cpu_speed_increment)
			self._computer.set_speed(
				self._cpu_speed + self._cpu_speed_increment)
			self._stat['last_diff'] = score_diff
			self._stat['level'] += 1
			pong_log.debug(
				f"Update speed, score diff = {score_diff}, last diff {self._stat['last_diff']}, level: {self._stat['level']}")

	# Move computer  to follow the ball after half of the game field
	def _move_computer(self):
		if self._ball.get_borders()['right'] < self._game_field.disp_w / 2:
			if self._computer.get_borders()['center_y'] < self._ball.get_borders()['center_y']:
				self._computer.set_speed(self._cpu_speed)
			else:
				self._computer.set_speed(-self._cpu_speed)
		else:
			self._computer.set_speed(0)

	# Based on incoming keyboard event, move the player
	def _move_player(self, event: pygame.event):
		if event.type == self._pong_pygame.KEYDOWN:
			if event.key == self._pong_pygame.K_UP:
				self._player.set_speed(-self._player_speed)
			if event.key == self._pong_pygame.K_DOWN:
				self._player.set_speed(self._player_speed)
		if event.type == self._pong_pygame.KEYUP:
			if event.key == self._pong_pygame.K_UP:
				self._player.set_speed(self._player_speed)
			if event.key == self._pong_pygame.K_DOWN:
				self._player.set_speed(-self._player_speed)	

	def _write_score(self):
		font_size = 30
		font = self._pong_pygame.font.SysFont("freemono", font_size)
		img = font.render(
			f'{self._stat["cpu_score"]}    {self._stat["player_score"]}', True, self._game_field.line_color)
		scor_str_len = len(
			str(f'{self._stat["cpu_score"]}    {self._stat["player_score"]}')) * font_size
		self._game_field.screen.blit(
			img, (((self._game_field.disp_w - scor_str_len) / 2) + 35, 10))
		
	def _write_win(self, winner_name: str):
		font_size = 30
		font = self._pong_pygame.font.SysFont("freemono", font_size)
		img = font.render(
			f'{winner_name} wins!', True, self._game_field.line_color)
		win_name_str = len(
			str(f'{winner_name} wins!')) * font_size
		self._game_field.screen.blit(
			img, (((self._game_field.disp_w - win_name_str) / 2) + 35, 10))
		self._pong_pygame.display.flip()

	# Check if cpu or player wins
	def _check_end_game(self):
		if self._stat['cpu_score'] == self._stat['max_score']:
			self._game_field.fill_screen()
			pong_log.info("End game, CPU wins!")
			self._write_win("CPU")
			sleep(2)
			self._pong_pygame.quit()
			sys.exit()
		if self._stat['player_score'] == self._stat['max_score']:
			self._game_field.fill_screen()
			pong_log.info(f"End game, {self._player.name} wins!")
			self._write_win(self._player.name)
			sleep(2)
			self._pong_pygame.quit()
			sys.exit()

	# Check for events like quit game, key press or game reset
	def _update_events(self):
		self._check_end_game()
		for event in self._pong_pygame.event.get():
			if event.type == self._pong_pygame.QUIT:
				self._pong_pygame.quit()
				sys.exit()
			# After a ball reset, waits for a player keypress to restart the ball
			if event.type == self._pong_pygame.KEYDOWN or event.type == self._pong_pygame.KEYUP:
				start_speed_x = get_random(1) * (self._BALL_SPEED_X_DFLT + (self._cpu_speed_increment * self._stat['level']))
				start_speed_y = self._BALL_SPEED_Y_DFLT + (self._cpu_speed_increment * self._stat['level'])
				if self._ball.get_speed()[0] == 0 and self._ball.get_speed()[1] == 0:
					self._ball.set_speed(start_speed_x, start_speed_y)
				self._move_player(event)

	def run_game(self):
		pong_log.info("Game start!")
		while True:
			self._check_collision()
			self._move_computer()
			self._update_events()
			self._game_field.fill_screen()
			self._ball.update_pos()
			self._player.update_pos()
			self._computer.update_pos()
			self._ball.draw(self._game_field.get_screen())
			self._player.draw(self._game_field.get_screen())
			self._computer.draw(self._game_field.get_screen())
			self._game_field.draw_borders()
			self._write_score()
			self._pong_pygame.display.flip()
			self._clock.tick(self._fps)


def main():
	os.remove(os.path.abspath(log_file))
	parser = argparse.ArgumentParser(description='Pong Game')
	parser.add_argument('-dw','--width', type=int, default=320, help='Width of the display (dflt 320)')
	parser.add_argument('-dh','--height', type=int, default=240, help='Height of the display (dflt 240)')
	parser.add_argument('-n','--name', type=str, default="player 1", help='Player name')
	parser.add_argument('-c', '--color', type=str, default="lightgrey", help='Game color (dflt light grey)')
	parser.add_argument('--fps', type=int, default=120, help='Framerate (dflt 120)')
	parser.add_argument('--max_score', type=int, default=10, help='Max score to win (dflt 10)')
	args = parser.parse_args()

	screen_width = args.width
	screen_height = args.height
	fps = args.fps
	max_score = args.max_score
	color = args.color
	player_name = args.name

	if color not in rgb_colors.keys():
		pong_log.error(f"Color {color} not found, setting light grey")
		color = "lightgrey"
	# Il resto del tuo codice rimane invariato

	game_field = GameField(screen_width, screen_height,
						   "black", rgb_colors[color], "Pong")
	ball = Ball(screen_width / 2, screen_height / 2, 5,
				rgb_colors[color], screen_width, screen_height)
	player = Gamer(screen_width - 30, (screen_height / 2) - 40,
				   10, 40, rgb_colors[color], player_name, screen_width, screen_height)
	computer = Gamer(20, (screen_height / 2) - 40, 10, 40,
					 rgb_colors[color], "CPU",screen_width, screen_height)

	pong = PongGame(game_field, ball, player, computer, fps=fps, max_score=max_score)

	pong.run_game()

if __name__ == '__main__':
	main()