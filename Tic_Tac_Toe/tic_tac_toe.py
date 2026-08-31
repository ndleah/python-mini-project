#cheat : high chance Win Strategy =>   1 - 8 - 6 - 5 - 4
#new version
import os

#initialize 
board = [' ' for x in range(10)]
FirstRun = True

#insert tic tac toe symbol to screen
def insertLetter(letter,pos):
    if(board.count(' ') >= 1):
        board[pos] = letter

def spaceIsFree(pos):
    return board[pos] == ' '

def printBoard(board):
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])

def isBoardFull(board):
    return board[1:].count(' ') == 0

def IsWinner(b, l):
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
    run = True
    while run:
        move = input("please select a position to enter the X between 1 to 9: ")
        try:
            move = int(move)
            if 1 <= move <= 9:
                if spaceIsFree(move):
                    run = False
                    insertLetter('X', move)
                else:
                    print('Sorry, this space is occupied')
            else:
                print('please type a number between 1 and 9')
        except ValueError:
            print('Please type a number')

def computerMove():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    move = 0

    for let in ['O', 'X']:
        for i in possibleMoves:
            boardcopy = board[:]
            boardcopy[i] = let
            if IsWinner(boardcopy, let):
                return i

    cornersOpen = [i for i in possibleMoves if i in [1, 3, 7, 9]]
    if len(cornersOpen) > 0:
        return selectRandom(cornersOpen)

    if 5 in possibleMoves:
        return 5

    edgesOpen = [i for i in possibleMoves if i in [2, 4, 6, 8]]
    if len(edgesOpen) > 0:
        return selectRandom(edgesOpen)

    return 0

def selectRandom(li):
    import random
    return random.choice(li)

def StartTheGame():
    global board
    board = [' ' for x in range(10)]
    CleanScreen()
    print('-------------------------')
    GamePlay()

def CleanScreen():
    try:
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    except Exception:
        pass

def TieGame():
    return isBoardFull(board) and (not (IsWinner(board, 'X') or IsWinner(board, 'O')))

scorecount = 0

def GamePlay():
    global scorecount
    if scorecount == 0:
        print("Welcome to the game!")
    if scorecount < 0:
        scorecount = 0
    printBoard(board)

    while not isBoardFull(board):
        if not IsWinner(board, 'O'):
            playerMove()
            CleanScreen()
            printBoard(board)
        else:
            scorecount -= 1
            print(f"Sorry, you lose 😢! Your Score is {scorecount}")
            break

        if IsWinner(board, 'X'):
            scorecount += 1
            print(f"You win! Your Score is {scorecount}")
            break

        if not isBoardFull(board):
            move = computerMove()
            if move != 0:
                insertLetter('O', move)
                print('computer placed an o on position', move, ':')
                CleanScreen()
                printBoard(board)
            if IsWinner(board, 'O'):
                scorecount -= 1
                print(f"Sorry, you lose 😢! Your Score is {scorecount}")
                break

def main():
    first_run = True
    while True:
        if first_run:
            first_run = False
            StartTheGame()
        else:
            if TieGame():
                print("It's a tie!")
            x = input("Do you want to play again? (y/n): ")
            if x.lower() in ('y', 'yes'):
                StartTheGame()
            else:
                print("GLHF")
                break

if __name__ == '__main__':
    main()