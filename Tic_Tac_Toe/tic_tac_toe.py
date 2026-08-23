# Cheat : High chance Win Strategy => 1 - 8 - 6 - 5 - 4
import os
import random

# Global board initialization (index 0 is unused, indices 1-9 represent board positions)
board = [' ' for _ in range(10)]
scorecount = 0


def insertLetter(letter, pos):
    """Inserts a letter ('X' or 'O') at the specified position if valid."""
    if 1 <= pos <= 9 and spaceIsFree(pos):
        board[pos] = letter


def spaceIsFree(pos):
    """Returns True if the position on the board is free."""
    return board[pos] == ' '


def printBoard(board):
    """Prints the 3x3 board to standard output."""
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])


def isBoardFull(board):
    """Checks if all playable spaces (1-9) are occupied."""
    return board[1:].count(' ') == 0


def IsWinner(b, l):
    """Checks if the specified letter 'l' has won on board 'b'."""
    return (
        (b[1] == l and b[2] == l and b[3] == l) or
        (b[4] == l and b[5] == l and b[6] == l) or
        (b[7] == l and b[8] == l and b[9] == l) or
        (b[1] == l and b[4] == l and b[7] == l) or
        (b[2] == l and b[5] == l and b[8] == l) or
        (b[3] == l and b[6] == l and b[9] == l) or
        (b[1] == l and b[5] == l and b[9] == l) or
        (b[3] == l and b[5] == l and b[7] == l)
    )


def playerMove():
    """Prompts the player to input their move and validates it."""
    run = True
    while run:
        move = input("Please select a position to enter 'X' (1-9): ")
        try:
            move = int(move)
            if 1 <= move <= 9:
                if spaceIsFree(move):
                    run = False
                    insertLetter('X', move)
                else:
                    print('Sorry, this space is occupied!')
            else:
                print('Please type a number between 1 and 9.')
        except ValueError:
            print('Please type a valid number.')


def computerMove():
    """Determines the best move for the computer."""
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    if not possibleMoves:
        return 0

    # 1. Check if computer can win or needs to block player win
    for let in ['O', 'X']:
        for i in possibleMoves:
            boardcopy = board[:]
            boardcopy[i] = let
            if IsWinner(boardcopy, let):
                return i

    # 2. Take open corners
    cornersOpen = [i for i in possibleMoves if i in [1, 3, 7, 9]]
    if cornersOpen:
        return selectRandom(cornersOpen)

    # 3. Take center
    if 5 in possibleMoves:
        return 5

    # 4. Take open edges
    edgesOpen = [i for i in possibleMoves if i in [2, 4, 6, 8]]
    if edgesOpen:
        return selectRandom(edgesOpen)

    return selectRandom(possibleMoves)


def selectRandom(li):
    """Selects a random item from a given list."""
    return random.choice(li)


def CleanScreen():
    """Clears terminal screen across platforms."""
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


def TieGame():
    """Checks if the current game is a tie."""
    return isBoardFull(board) and not IsWinner(board, 'X') and not IsWinner(board, 'O')


def GamePlay():
    """Main gameplay loop for a single round."""
    global scorecount
    if scorecount == 0:
        print("Welcome to the game!")
    elif scorecount < 0:
        scorecount = 0
    printBoard(board)

    while not isBoardFull(board):
        # --- Player's Turn ---
        playerMove()
        CleanScreen()
        printBoard(board)

        # Check if Player won
        if IsWinner(board, 'X'):
            scorecount += 1
            print(f"\nYou win! Your Score is {scorecount}")
            return

        # Check for tie after Player move
        if isBoardFull(board):
            print("\nIt's a tie!")
            return

        # --- Computer's Turn ---
        move = computerMove()
        if move != 0:
            insertLetter('O', move)
            CleanScreen()
            print(f"Computer placed an 'O' on position {move}:\n")
            printBoard(board)

        # Check if Computer won
        if IsWinner(board, 'O'):
            scorecount = max(0, scorecount - 1)
            print(f"\nSorry, you lose! Your Score is {scorecount}")
            return

        # Check for tie after Computer move
        if isBoardFull(board):
            print("\nIt's a tie!")
            return


def StartTheGame():
    """Resets the board and starts a new round."""
    global board
    board = [' ' for _ in range(10)]
    CleanScreen()
    print('-------------------------')
    GamePlay()


def main():
    """Main application loop handling game rounds and replay prompt."""
    while True:
        StartTheGame()
        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ('y', 'yes'):
            print("\nGLHF!")
            break


if __name__ == '__main__':
    main()