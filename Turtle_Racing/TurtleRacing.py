import turtle
import random
import time

# Configurable track dimensions
WIDTH, HEIGHT = 800, 600

# High-contrast, vibrant turtle colors suited for dark background (black removed)
COLORS = ['red', 'green', 'blue', 'orange', 'yellow', 'white', 'purple', 'pink', 'cyan', 'lime']

def init_turtle():
    """Initializes the turtle graphics window with a sleek dark slate background."""
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title('Turtle Racing!')
    screen.bgcolor('#1e1e24')
    return screen

def get_number_of_racers(screen):
    """Prompts the user inside the GUI for the number of racers."""
    try:
        racers = screen.numinput(
            "Number of Racers",
            "Enter the number of racers (2 - 10):",
            default=5,
            minval=2,
            maxval=10
        )
        if racers is None:
            return None
        return int(racers)
    except Exception:
        return None

def draw_track(colors, screen):
    """Draws the start/finish lines and lane dividers instantly on the canvas."""
    # Temporarily turn off tracer for instantaneous drawing
    screen.tracer(0)
    
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.color("white")
    pen.pensize(2)

    spacingx = WIDTH // (len(colors) + 1)
    start_y = -HEIGHT // 2 + 50
    finish_y = HEIGHT // 2 - 50

    # Draw Starting Line
    pen.penup()
    pen.goto(-WIDTH // 2, start_y)
    pen.pendown()
    pen.forward(WIDTH)

    # Draw Finish Line (lime dashed line)
    pen.penup()
    pen.goto(-WIDTH // 2, finish_y)
    dash_length = 20
    is_down = True
    pen.color("lime")
    pen.pensize(4)
    while pen.xcor() < WIDTH // 2:
        if is_down:
            pen.pendown()
        else:
            pen.penup()
        pen.forward(dash_length)
        is_down = not is_down

    # Draw Lanes / Boundaries
    pen.color("#3a3a44")
    pen.pensize(1)
    for i in range(len(colors) - 1):
        x = -WIDTH // 2 + (i + 1.5) * spacingx
        pen.penup()
        pen.goto(x, start_y)
        pen.setheading(90)
        while pen.ycor() < finish_y:
            pen.pendown()
            pen.forward(15)
            pen.penup()
            pen.forward(15)

    # Update screen and restore normal tracer
    screen.update()
    screen.tracer(1)

def countdown(screen):
    """Displays a graphical countdown in the center of the track."""
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("white")
    writer.goto(0, 0)
    
    for msg in ["3", "2", "1", "GO!"]:
        writer.clear()
        writer.write(msg, align="center", font=("Arial", 48, "bold"))
        screen.update()
        time.sleep(0.6)
    writer.clear()
    screen.update()

def announce_winner(color):
    """Draws a beautiful card in the center to highlight the winner."""
    announcer = turtle.Turtle()
    announcer.hideturtle()
    announcer.speed(0)
    announcer.penup()
    
    # Draw dark background panel card
    announcer.goto(-200, 50)
    announcer.color("#0f0f12")
    announcer.begin_fill()
    for _ in range(2):
        announcer.forward(400)
        announcer.right(90)
        announcer.forward(100)
        announcer.right(90)
    announcer.end_fill()
    
    # Write "Race Finished" subtitle
    announcer.goto(0, -25)
    announcer.color("white")
    announcer.write("Race Finished!", align="center", font=("Arial", 14, "normal"))
    
    # Write Winner color text
    announcer.goto(0, 5)
    display_color = color.upper()
    announcer.color(color)
    announcer.write(f"{display_color} Turtle Wins!", align="center", font=("Arial", 22, "bold"))

def create_turtles(colors):
    """Creates the racers and places them at their lane starting points."""
    turtles = []
    spacingx = WIDTH // (len(colors) + 1)
    start_y = -HEIGHT // 2 + 50
    for i, color in enumerate(colors):
        racer = turtle.Turtle()
        racer.color(color)
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        racer.setpos(-WIDTH//2 + (i + 1) * spacingx, start_y)
        racer.pendown()
        racer.pensize(3)
        racer.speed(2)
        turtles.append(racer)

    return turtles

def race(colors, screen):
    """Moves the turtles forward randomly until one crosses the finish line."""
    turtles = create_turtles(colors)
    finish_y = HEIGHT // 2 - 50
    while True:
        for racer in turtles:
            distance = random.randrange(1, 15)
            racer.forward(distance)

            x, y = racer.pos()
            if y >= finish_y:
                winner_color = colors[turtles.index(racer)]
                announce_winner(winner_color)
                return winner_color

def main():
    try:
        screen = init_turtle()
        racers = get_number_of_racers(screen)
        if racers is None:
            print("Game closed/cancelled.")
            return

        random.shuffle(COLORS)
        colors = COLORS[:racers]

        draw_track(colors, screen)
        countdown(screen)
        
        winner = race(colors, screen)
        if winner:
            print("The winner is the turtle with color:", winner)
            
            # Exit instructions
            exit_msg = turtle.Turtle()
            exit_msg.hideturtle()
            exit_msg.penup()
            exit_msg.color("gray")
            exit_msg.goto(0, -HEIGHT // 2 + 15)
            exit_msg.write("Click anywhere on the screen to exit.", align="center", font=("Arial", 10, "italic"))
            screen.exitonclick()
    except (turtle.Terminator, Exception):
        print("Application closed or interrupted.")

if __name__ == "__main__":
    main()