from random import sample


def generate_board(num):
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return sample(s, len(s))

    # randomize rows, col, num
    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # randomized baseline
    board_tmp = [[nums[pattern(r, c)] for c in cols] for r in rows]

    # print full board
    print("=======full board========")
    print_board(board_tmp)

    # remove numbers of the board
    squares = side * side
    if num == 0:
        # default number of empty slots
        empties = squares * 3 // 4
    else:
        # given number of empty slots
        empties = 81 - num
    # looping a randomized board for the amount of empty mubers
    for p in sample(range(squares), empties):
        # set nubers to 0 of the randomized board
        board_tmp[p // side][p % side] = 0

    # returning the generated board
    return board_tmp


"""
This solution works, but it could create boards that are not possible.

def generate_board(num):
    bo = [[0 for x in range(9)] for y in range(9)]
    for i in range(9):
        for j in range(9):
            bo[i][j] = 0

    for i in range(num):
        row = random.randrange(9)
        col = random.randrange(9)
        num = random.randrange(1, 10)

        while not possible(bo, (row, col), num) or bo[row][col] != 0:
            row = random.randrange(9)
            col = random.randrange(9)
            num = random.randrange(1, 10)
        bo[row][col] = num

    return bo
"""


def print_board(bo):
    # looping every line in the array
    for i in range(len(bo)):
        # printing line if the vertical "box" changes
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        # looping every character in one line
        for j in range(len(bo[0])):
            # printing lines if the horizontal box changes
            # printing each character with spaces except for the last
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                # last character is printed without spaces behind
                print(bo[i][j])
            else:
                # printing each character with spaces
                print(str(bo[i][j]) + " ", end="")
    print("")


def possible(bo, pos, num):
    # checking row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            # not possible
            return False

    # checking column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            # not possible
            return False

    # checking square
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):  # row
        for j in range(box_x * 3, box_x * 3 + 3):  # col
            if bo[i][j] == num and (i, j) != pos:
                # not possible number
                return False
    # possible number
    return True


def next_empty(bo):
    # searching for the next 0 on the board
    for i in range(len(bo)):
        # looping rows
        for j in range(len(bo[0])):
            # looping columns
            if bo[i][j] == 0:
                return i, j  # returning row and column


def solve(bo):
    # searching for next empty solt
    slot = next_empty(bo)
    if not slot:
        # return True if there is no empty slot
        return True
    else:
        row, col = slot
    # looping number 1 to 9
    for i in range(1, 10):
        # check if the number is possible in this location
        if possible(bo, (row, col), i):
            # placing the number on the board
            bo[row][col] = i

            # starting recursion
            if solve(bo):
                # returns True when the previous returned True
                # This will only activate if the board is full
                return True

            # resetting the changed value to 0
            bo[row][col] = 0
    return False


# Fill your numbers in the board below or create a new array to solve the board you give.
board = [
    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 0],

    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 0],

    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [0, 0, 0,   0, 0, 0,   0, 0, 0]
]

# use this function to generate a new board
# comment and use the array above to solve manual preset boards.
board = generate_board(0)


# printing the unsolved board
print("======solvable board=====")
print_board(board)

# solving the board
solve(board)

# printing the board
print("======solved board=======")
print_board(board)
