import turtle as t
import random as rd

t.bgcolor('yellow')

caterpillar = t.Turtle()
caterpillar.shape('square')
caterpillar.speed(0)
caterpillar.penup()
caterpillar.hideturtle()

leaf = t.Turtle()
leaf_shape = ((0, 0), (14, 2), (18, 6), (20, 20), (6, 18), (2, 14))
t.register_shape('leaf', leaf_shape)
leaf.shape('leaf')
leaf.color('green')
leaf.penup()
leaf.hideturtle()

game_started = False
text_turtle = t.Turtle()
text_turtle.hideturtle()
text_turtle.penup()

score_turtle = t.Turtle()
score_turtle.hideturtle()
score_turtle.speed(0)

game_over_turtle = t.Turtle()
game_over_turtle.hideturtle()
game_over_turtle.penup()

num_obstacles = 5
obstacles = []

for _ in range(num_obstacles):
    new_obstacle = t.Turtle()
    new_obstacle.shape('circle')
    new_obstacle.color('red')
    new_obstacle.penup()
    new_obstacle.hideturtle()
    obstacles.append(new_obstacle)

def outside_window():
    left_wall = -t.window_width() / 2
    right_wall = t.window_width() / 2
    top_wall = t.window_height() / 2
    bottom_wall = -t.window_height() / 2
    x, y = caterpillar.pos()
    return x < left_wall or x > right_wall or y > top_wall or y < bottom_wall

def game_over():
    global game_started
    game_started = False
    caterpillar.color('yellow')
    leaf.color('yellow')
    game_over_turtle.clear()
    game_over_turtle.goto(0, 0)
    game_over_turtle.write('GAME OVER !', align='center', font=('Arial', 30, 'bold'))
    text_turtle.goto(0, -50)
    text_turtle.write('Press SPACE to restart', align='center', font=('Arial', 18, 'bold'))

def display_score(current_score):
    score_turtle.clear()
    score_turtle.penup()
    x = (t.window_width() / 2) - 70
    y = (t.window_height() / 2) - 70
    score_turtle.setpos(x, y)
    score_turtle.write(str(current_score), align='right', font=('Arial', 40, 'bold'))

def place_leaf():
    leaf.hideturtle()
    leaf.setx(rd.randint(-200, 200))
    leaf.sety(rd.randint(-200, 200))
    leaf.showturtle()

def place_obstacles():
    for obs in obstacles:
        obs.hideturtle()
        obs.setposition(rd.randint(-200, 200), rd.randint(-200, 200))
        obs.showturtle()

caterpillar_speed = 2
caterpillar_length = 3
score = 0

def start_game():
    global game_started, caterpillar_speed, caterpillar_length, score
    if game_started:
        return
    game_started = True

    text_turtle.clear()
    game_over_turtle.clear()

    score = 0
    caterpillar_speed = 2
    caterpillar_length = 3

    caterpillar.goto(0, 0)
    caterpillar.setheading(0)
    caterpillar.color('black')
    caterpillar.shapesize(1, caterpillar_length, 1)
    caterpillar.showturtle()

    leaf.color('green')
    display_score(score)
    place_leaf()
    place_obstacles()

    game_loop()

def game_loop():
    global game_started, caterpillar_speed, caterpillar_length, score
    if not game_started:
        return

    caterpillar.forward(caterpillar_speed)

    # Check leaf collision
    if caterpillar.distance(leaf) < 20:
        place_leaf()
        caterpillar_length += 1
        caterpillar.shapesize(1, caterpillar_length, 1)
        caterpillar_speed += 0.5
        score += 10
        display_score(score)

    # Check obstacle collision
    for obstacle in obstacles:
        if caterpillar.distance(obstacle) < 20:
            game_over()
            return

    # Check boundary collision
    if outside_window():
        game_over()
        return

    t.ontimer(game_loop, 50)

def move_up():
    if caterpillar.heading() != 270:
        caterpillar.setheading(90)

def move_down():
    if caterpillar.heading() != 90:
        caterpillar.setheading(270)

def move_left():
    if caterpillar.heading() != 0:
        caterpillar.setheading(180)

def move_right():
    if caterpillar.heading() != 180:
        caterpillar.setheading(0)

text_turtle.goto(0, 0)
text_turtle.write('Press SPACE to start', align='center', font=('Arial', 18, 'bold'))

t.onkey(start_game, 'space')
t.onkey(move_up, 'Up')
t.onkey(move_right, 'Right')
t.onkey(move_down, 'Down')
t.onkey(move_left, 'Left')
t.listen()

if __name__ == '__main__':
    t.mainloop()

