import tkinter as tk

# Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER_1 = 1
PLAYER_2 = 2

# Initialize board
board = [[EMPTY] * COLS for _ in range(ROWS)]
current_player = PLAYER_1

def drop_piece(col):
    global current_player
    row = get_next_open_row(col)
    if row is not None:
        board[row][col] = current_player
        draw_board()
        if check_winner(row, col):
            print(f"Player {current_player} wins!")
            reset_board()
        else:
            current_player = 3 - current_player  # Switch player

def get_next_open_row(col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None

def check_winner(row, col):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        count = 1 + check_line(row, col, dr, dc) + check_line(row, col, -dr, -dc)
        if count >= 4:
            return True
    return False

def check_line(row, col, delta_row, delta_col):
    count = 0
    while 0 <= row + delta_row < ROWS and 0 <= col + delta_col < COLS and \
            board[row][col] == board[row + delta_row][col + delta_col]:
        count += 1
        row += delta_row
        col += delta_col
    return count

def draw_board():
    canvas.delete("all")  # Clear previous drawings

    cell_size = 50
    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

            color = "white" if board[row][col] == EMPTY else ("red" if board[row][col] == PLAYER_1 else "yellow")
            canvas.create_oval(x1, y1, x2, y2, fill=color)

def reset_board():
    global board, current_player
    board = [[EMPTY] * COLS for _ in range(ROWS)]
    current_player = PLAYER_1
    draw_board()

# Create the main window
root = tk.Tk()
root.title("Connect 4")

# Create buttons at the bottom
buttons = []
for col in range(COLS):
    button = tk.Button(root, text=str(col + 1), command=lambda col=col: drop_piece(col))
    button.grid(row=ROWS, column=col)
    buttons.append(button)

# Create the game board
canvas = tk.Canvas(root, width=350, height=300)
canvas.grid(row=0, column=0, rowspan=ROWS, columnspan=COLS)

# Initial drawing of the board
draw_board()

# Run the main loop
root.mainloop()
