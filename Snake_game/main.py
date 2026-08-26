import os
import sys
import time
import random
import pygame

white = (255, 255, 255)
black = (36, 36, 36)
red = (213, 50, 80)
green = (0, 255, 0)

display_width = 600
display_height = 500
snake_block = 10
snake_speed = 15

def score(display, score_val):
    score_font = pygame.font.SysFont("arial", 15)
    value = score_font.render(" Score: " + str(score_val), True, white)
    display.blit(value, [0, 0])

def snake(display, snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, green, [x[0], x[1], snake_block_size, snake_block_size], border_radius=3)

def message(display, msg, color, size=12):
    font_style = pygame.font.SysFont("bahnschrift", size)
    mesg = font_style.render(msg, True, color)
    display.blit(mesg, [display_width / 8, display_height / 5])

def gameLoop(display, clock):
    game_over = False
    game_close = False

    x1 = display_width / 2
    y1 = display_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            display.fill(black)
            message(display, "You Lost! Press Space Again or Q to Quit", red, 25)
            score(display, Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop(display, clock)
                        return
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                # Prevent 180-degree instant reversal
                if (event.key in (pygame.K_a, pygame.K_LEFT)) and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif (event.key in (pygame.K_d, pygame.K_RIGHT)) and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif (event.key in (pygame.K_w, pygame.K_UP)) and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif (event.key in (pygame.K_s, pygame.K_DOWN)) and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        display.fill(black)
        pygame.draw.rect(display, red, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake(display, snake_block, snake_List)
        score(display, Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

def main():
    pygame.init()
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Snake Game')

    icon_path = os.path.join(os.path.dirname(__file__), "snakeicon.ico")
    if os.path.exists(icon_path):
        try:
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        except Exception:
            pass

    clock = pygame.time.Clock()
    gameLoop(display, clock)
    pygame.quit()

if __name__ == '__main__':
    main()

