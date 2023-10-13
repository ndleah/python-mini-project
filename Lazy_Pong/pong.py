import pygame
import sys
import random


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
		self._time_per_px = 1 / fps
		self._max_ball_time_4_travel = 3
		self._max_gamer_time_4_travel = 4
		self._pong_pygame = pygame
		self._game_field = game_field
		self._ball = ball
		self._player = player
		self._computer = computer
		self._pong_pygame.init()
		self._clock = self._pong_pygame.time.Clock()
		self._stat = {"player": 0, "cpu": 0,
					   "last_diff": 0, "level": 1, "max_score": max_score}

		self._fps = fps
		self._BALL_SPEED_X_DFLT = self._game_field.disp_w / self._max_ball_time_4_travel * self._time_per_px
		self._BALL_SPEED_Y_DFLT = self._game_field.disp_h / self._max_ball_time_4_travel * self._time_per_px
		self._CPU_SPEED_DFLT = self._game_field.disp_h / self._max_gamer_time_4_travel * self._time_per_px
		self._game_speed_increment = 0.5
		self._player_speed = 4
		self._cpu_speed = self._CPU_SPEED_DFLT

	def _reset_game(self):
		self._ball.reset()
		self._player.reset()
		self._computer.reset()
		self._update_game_speed()

	def _check_collision(self):
		ball_coord = self._ball.get_borders()
		if ball_coord['left'] <= self._computer.get_borders()['left']:
			print("Player score +1")
			self._stat['player'] += 1
			self._reset_game()

		if ball_coord['right'] >= self._player.get_borders()['right']:
			print("CPU score +1")
			self._stat['cpu'] += 1
			self._reset_game()

		if ball_coord['right'] > self._game_field.disp_w / 2 and ball_coord['right'] >= self._player.get_borders()['left']:
			if ball_coord['top'] <= self._player.get_borders()['bott'] and ball_coord['bott'] >= self._player.get_borders()['top']:
				self._ball.invert_move(invert_x=True)

		if ball_coord['left'] < self._game_field.disp_w / 2 and ball_coord['left'] <= self._computer.get_borders()['right']:
			if ball_coord['top'] <= self._computer.get_borders()['bott'] and ball_coord['bott'] >= self._computer.get_borders()['top']:
				self._ball.invert_move(invert_x=True)

	def _update_game_speed(self):
		score_diff = self._stat['player'] - self._stat['cpu']
		if score_diff > 0 and score_diff > self._stat['last_diff']:
			self._ball.set_speed(abs(self._ball.get_speed()[
								 0]) + self._game_speed_increment, abs(self._ball.get_speed()[1]) + self._game_speed_increment)
			self._computer.set_speed(
				self._cpu_speed + self._game_speed_increment)
			self._stat['last_diff'] = score_diff
			self._stat['level'] += 1
			print(
				f"Update speed, score diff = {score_diff}, last diff {self._stat['last_diff']}, level: {self._stat['level']}")

	def _move_computer(self):
		if self._ball.get_borders()['right'] < self._game_field.disp_w / 2:
			if self._computer.get_borders()['center_y'] < self._ball.get_borders()['center_y']:
				self._computer.set_speed(self._cpu_speed)
			else:
				self._computer.set_speed(-self._cpu_speed)
		else:
			self._computer.set_speed(0)

	def _update_events(self):
		if self._stat['cpu'] == self._stat['max_score']:
			print("End game, CPU wins!")
			self._pong_pygame.quit()
			sys.exit()
		if self._stat['player'] == self._stat['max_score']:
			print("End game, Player wins!")
			self._pong_pygame.quit()
			sys.exit()
		for event in self._pong_pygame.event.get():
			if event.type == self._pong_pygame.QUIT:
				self._pong_pygame.quit()
				sys.exit()
			# After a ball reset, waits for a player keypress to restart the ball
			if event.type == self._pong_pygame.KEYDOWN or event.type == self._pong_pygame.KEYUP:
				start_speed_x = get_random(1) * (self._BALL_SPEED_X_DFLT + (self._game_speed_increment * self._stat['level']))
				start_speed_y = self._BALL_SPEED_Y_DFLT + (self._game_speed_increment * self._stat['level'])
				if self._ball.get_speed()[0] == 0 and self._ball.get_speed()[1] == 0:
					self._ball.set_speed(start_speed_x, start_speed_y)
			if event.type == self._pong_pygame.KEYDOWN:
				if event.key == self._pong_pygame.K_UP:
					self._player.set_speed(-self._player_speed)
					print(f"Player speed updated: {self._player.get_speed()}")
				if event.key == self._pong_pygame.K_DOWN:
					self._player.set_speed(self._player_speed)
					print(f"Player speed updated: {self._player.get_speed()}")
			if event.type == self._pong_pygame.KEYUP:
				if event.key == self._pong_pygame.K_UP:
					self._player.set_speed(self._player_speed)
					print(f"Player speed updated: {self._player.get_speed()}")
				if event.key == self._pong_pygame.K_DOWN:
					self._player.set_speed(-self._player_speed)
					print(f"Player speed updated: {self._player.get_speed()}")

	def _write_score(self):
		font_size = 30
		font = self._pong_pygame.font.SysFont("freemono", font_size)
		img = font.render(
			f'{self._stat["cpu"]}    {self._stat["player"]}', True, self._game_field.line_color)
		scor_str_len = len(
			str(f'{self._stat["cpu"]}    {self._stat["player"]}')) * font_size
		self._game_field.screen.blit(
			img, (((self._game_field.disp_w - scor_str_len) / 2) + 35, 10))

	def run_game(self):
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
	screen_width = 240	
	screen_height = 120
	light_grey = (200, 200, 200)

	game_field = GameField(screen_width, screen_height,
						   "black", light_grey, "Pong")
	ball = Ball(screen_width / 2, screen_height / 2, 5,
				light_grey, screen_width, screen_height)
	player = Gamer(screen_width - 30, (screen_height / 2) - 40,
				   10, 40, light_grey, screen_width, screen_height)
	computer = Gamer(20, (screen_height / 2) - 40, 10, 40,
					 light_grey, screen_width, screen_height)

	pong = PongGame(game_field, ball, player, computer, fps=120, max_score=10)

	pong.run_game()


if __name__ == '__main__':
	main()
