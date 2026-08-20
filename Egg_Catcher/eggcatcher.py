from itertools import cycle
from random import randrange
from tkinter import Tk, Canvas, messagebox

# Game setup variables
canvas_width = 800
canvas_height = 400

# Initialize the main window
win = Tk()
win.title("Egg Catcher")
c = Canvas(win, width=canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill='sea green', width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

# Game design variables
color_cycle = cycle(['light blue', 'light pink', 'light yellow', 'light green', 'red', 'blue', 'green', 'black'])
egg_width = 45
egg_height = 55
egg_score = 10

INITIAL_EGG_SPEED = 500
INITIAL_EGG_INTERVAL = 4000
MIN_EGG_SPEED = 100
MIN_EGG_INTERVAL = 800
difficulty_factor = 0.95

egg_speed = INITIAL_EGG_SPEED
egg_interval = INITIAL_EGG_INTERVAL

# Catcher setup
catcher_color = 'blue'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x, catcher_start_y, catcher_start_x2, catcher_start_y2, start=200, extent=140, style='arc', outline=catcher_color, width=3)

# Score and lives setup
score = 0
score_text = c.create_text(10, 10, anchor='nw', font=('Arial', 18, 'bold'), fill='darkblue', text='Score : ' + str(score))

lives_remaning = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=('Arial', 18, 'bold'), fill='darkblue', text='Lives : ' + str(lives_remaning))

eggs = []

# Timer tracking IDs to prevent stacking multiple loops on restart
timer_create = None
timer_move = None
timer_catch = None
game_running = True

def cancel_timers():
    global timer_create, timer_move, timer_catch
    if timer_create:
        win.after_cancel(timer_create)
        timer_create = None
    if timer_move:
        win.after_cancel(timer_move)
        timer_move = None
    if timer_catch:
        win.after_cancel(timer_catch)
        timer_catch = None

# Function to create eggs at random positions
def create_eggs():
    global timer_create
    if not game_running:
        return
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    timer_create = win.after(egg_interval, create_eggs)

# Function to move eggs downwards
def move_eggs():
    global timer_move
    if not game_running:
        return
    for egg in eggs[:]:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        c.move(egg, 0, 10)
        if egg_y2 > canvas_height:
            egg_dropped(egg)
            if not game_running:
                break
    if game_running:
        timer_move = win.after(egg_speed, move_eggs)

# Function to handle egg drop events
def egg_dropped(egg):
    global lives_remaning, game_running
    if egg in eggs:
        eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaning <= 0:
        game_running = False
        cancel_timers()
        # Prompt the player to play again or exit
        response = messagebox.askyesno('GAME OVER!', 'Final Score: ' + str(score) + '\nDo you want to play again?')
        if response:
            reset_game()  # Reset the game if the player chooses to play again
        else:
            win.destroy()  # Close the game if the player chooses not to play again

# Function to reset the game state for a new game
def reset_game():
    global score, lives_remaning, eggs, egg_speed, egg_interval, game_running
    cancel_timers()
    for egg in eggs:
        c.delete(egg)
    eggs = []
    score = 0
    lives_remaning = 3
    egg_speed = INITIAL_EGG_SPEED
    egg_interval = INITIAL_EGG_INTERVAL
    c.itemconfigure(score_text, text='Score : ' + str(score))
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaning))
    game_running = True
    # Restart egg creation and movement
    win.after(1000, start_game_loops)

def start_game_loops():
    global timer_create, timer_move, timer_catch
    cancel_timers()
    if game_running:
        timer_create = win.after(0, create_eggs)
        timer_move = win.after(0, move_eggs)
        timer_catch = win.after(0, catch_check)

# Function to decrease lives
def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaning))

# Function to check if eggs are caught
def catch_check():
    global timer_catch
    if not game_running:
        return
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
    for egg in eggs[:]:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
            if egg in eggs:
                eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    if game_running:
        timer_catch = win.after(100, catch_check)

# Function to increase the score
def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = max(MIN_EGG_SPEED, int(egg_speed * difficulty_factor))
    egg_interval = max(MIN_EGG_INTERVAL, int(egg_interval * difficulty_factor))
    c.itemconfigure(score_text, text='Score : ' + str(score))

# Event handlers for moving the catcher
def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

# Start the game processes
start_game_loops()

win.mainloop()

