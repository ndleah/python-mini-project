import numpy as np

class Board:
    WHITE = -1
    BLACK =  1
    EMPTY =  0

    DIRECTIONS = (  ( 1, 0),    # right
                    (-1, 0),    # left
                    ( 0, 1),    # down
                    (-1, 1),    # downwards left
                    ( 1, 1),    # downwards right
                    ( 0,-1),    # up
                    (-1,-1),    # upwards left
                    ( 1,-1),    # upwards right
                )

    def __init__(self) -> None:
        '''Initiliaze the Othello game board with a 8x8 numpy matrix'''
        self.board = np.array([0]*8, dtype = np.int8)   # initiliasing 1D array with the first row of 8 zeroes
        self.board = self.board[np.newaxis, : ]         # expanding 1D array to 2D array
        for _ in range(3):                              # increasing rows till 8
            self.board = np.concatenate((self.board, self.board), axis = 0)

        # initiliasing the centre squares
        self.board[3, 3] = self.board[4,4] = Board.WHITE
        self.board[3, 4] = self.board[4,3] = Board.BLACK

        self.black_disc_count = 2
        self.white_disc_count = 2
    
    @staticmethod
    def checkCoordRange(x: int, y: int) -> bool:
        '''Returns true if the given parameters represent an actual cell in a 8x8 matrix'''

        return (x >= 0 and y >= 0) and (x < 8 and y < 8)

    def all_legal_moves(self, PLAYER: int) -> set:
        '''Return all legal moves for the player'''

        all_legal_moves = set()
        for row in range(8):
            for col in range(8):
                if self.board[row, col] == PLAYER:
                    all_legal_moves.update(self.legal_moves(row, col))
        
        return all_legal_moves

    def legal_moves(self, r: int, c: int) -> list:
        '''Return all legal moves for the cell at the given position'''

        PLAYER = self.board[r, c]
        OPPONENT = PLAYER * -1

        legal_moves = []
        for dir in Board.DIRECTIONS:
            rowDir, colDir = dir
            row = r + rowDir
            col = c + colDir
                
            if Board.checkCoordRange(row, col) is False or self.board[row, col] != OPPONENT:
                continue
            
            row += rowDir
            col += colDir
            while (Board.checkCoordRange(row, col) is True and self.board[row, col] == OPPONENT):
                row += rowDir
                col += colDir
            if (Board.checkCoordRange(row, col) is True and self.board[row, col] == Board.EMPTY):   # possible move
                legal_moves.append((row, col))

        return legal_moves

    def flipDiscs(self, PLAYER: int, initCoords: tuple[int, int], endCoords: tuple[int, int], direction: tuple[int, int]):
        '''Flip the discs between the given two cells to the given PLAYER color.'''

        OPPONENT = PLAYER * -1
        rowDir, colDir = direction

        row, col = initCoords
        row += rowDir
        col += colDir 

        r, c = endCoords

        while (self.board[row, col] == OPPONENT) and (row != r or col != c):
            self.board[row, col] = PLAYER
            row += rowDir
            col += colDir

    def set_discs(self, row: int, col: int, PLAYER: int) -> None:
        '''Set the discs on the board as per the move made on the given cell'''
        
        self.board[row, col] = PLAYER
        OPPONENT = PLAYER * - 1
        
        for dir in Board.DIRECTIONS:
            rowDir, colDir = dir
            r = row + rowDir
            c = col + colDir

            if Board.checkCoordRange(r, c) is False or self.board[r, c] != OPPONENT:
                continue
            
            r += rowDir
            c += colDir
            while (Board.checkCoordRange(r, c) is True and self.board[r, c] == OPPONENT):
                r += rowDir
                c += colDir
            if (Board.checkCoordRange(r, c) is True and self.board[r, c] == PLAYER):
                self.flipDiscs(PLAYER, (row, col), (r, c), dir) 
                
        # update disc counters
        self.black_disc_count = self.board[self.board > 0].sum()
        self.white_disc_count = -self.board[self.board < 0].sum()

    def print_board(self) -> None:
        print(self.board)

    def reset_board(self) -> None:
        self.board.fill(Board.EMPTY)

        # initiliasing the centre squares
        self.board[3, 3] = self.board[4,4] = Board.WHITE
        self.board[3, 4] = self.board[4,3] = Board.BLACK

        self.black_disc_count = self.white_disc_count = 2

    def check_game_over(self) -> bool:
        possibleBlackMoves = self.all_legal_moves(Board.BLACK)
        possibleWhiteMoves = self.all_legal_moves(Board.WHITE)

        if possibleBlackMoves or possibleWhiteMoves:
            return False
        return True
    
    def evaluate_board(self) -> int:
        '''Evaluate the board as per various heuristics.'''

        # coin parity heuristic
        coin_parity = 100 * (self.black_disc_count - self.white_disc_count) / (self.black_disc_count + self.white_disc_count)
        
        # mobility heuristic value
        black_mobility = len(self.all_legal_moves(Board.BLACK))
        white_mobility = len(self.all_legal_moves(Board.WHITE))
        if black_mobility + white_mobility == 0:
            actual_mobility = 0
        else:
            actual_mobility = 100 * (black_mobility - white_mobility) / (black_mobility + white_mobility)

        # corner heuristic value
        corners = (self.board[0, 0], self.board[0,7], self.board[7, 0], self.board[7, 7])
        black_corners = sum(+20 for coin in corners if coin == Board.BLACK)
        white_corners = sum(-20 for coin in corners if coin == Board.WHITE)
        if black_corners + white_corners == 0:
            corner_value = 0
        else:
            corner_value = 100 * (black_corners - white_corners) / (black_corners + white_corners)

        return coin_parity + actual_mobility + corner_value