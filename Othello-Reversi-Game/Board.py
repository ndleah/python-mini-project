import numpy as np

class Board:
    WHITE = -1
    BLACK =  1
    EMPTY =  0

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

    def all_legal_moves(self, PLAYER: int) -> set:
        '''Return all legal moves for the player'''
        OPPONENT = Board.WHITE if PLAYER == Board.BLACK else Board.BLACK

        all_legal_moves = set()
        for row in range(8):
            for col in range(8):
                if self.board[row, col] == PLAYER:
                    all_legal_moves.update(self.legal_moves(row, col))
        
        return all_legal_moves

    def legal_moves(self, row: int, col: int) -> list:
        '''Return all legal moves for the cell at the given position'''
        PLAYER = self.board[row, col]
        OPPONENT = Board.WHITE if PLAYER == Board.BLACK else Board.BLACK
        legal_moves = list()

        # check for legal moves along the row of the cell
        if col >= 2:
            i = col - 1
            while i >= 0 and self.board[row, i] == OPPONENT:
                i -= 1
            if (i != col - 1 and i >= 0) and self.board[row, i] == Board.EMPTY:
                legal_moves.append((row, i))

        if col <= 5:
            i = col + 1
            while i < 8 and self.board[row, i] == OPPONENT:
                i += 1
            if (i != col + 1 and i < 8) and self.board[row, i] == Board.EMPTY:
                legal_moves.append((row, i))

        # check for legal moves along the column of the cell
        if row >= 2:
            i = row - 1
            while i >= 0 and self.board[i, col] == OPPONENT:
                i -= 1
            if (i != row - 1 and i >= 0) and self.board[i, col] == Board.EMPTY:
                legal_moves.append((i, col))

        if row <= 5:
            i = row + 1
            while i < 8 and self.board[i, col] == OPPONENT:
                i += 1
            if (i != row + 1 and i < 8) and self.board[i,col] == Board.EMPTY:
                legal_moves.append((i, col))

        # check for legal moves along diagonals on which the cell lies
        if row >= 2 and col >= 2:   # diagonal from the cell towards top left
            r = row - 1
            c = col - 1
            while (r >= 0 and c >= 0) and self.board[r, c] == OPPONENT: 
                r -= 1
                c -=1
            if (r != row - 1 and c != col - 1) and (r >= 0 and c >= 0) and self.board[r, c] == Board.EMPTY:
                legal_moves.append((r, c))
            
        if row >= 2 and col <= 5:   # diagonal from the cell towards top right
            r = row - 1
            c = col + 1
            while (r >= 0 and c < 8) and self.board[r, c] == OPPONENT:
                r -= 1
                c +=1
            if (r != row - 1 and c != col + 1) and (r >= 0 and c < 8) and self.board[r, c] == Board.EMPTY:
                legal_moves.append((r, c))

        if row <= 5 and col <= 5:   # diagonal from the cell towards bottom right
            r = row + 1
            c = col + 1
            while (r < 8 and c < 8) and self.board[r, c] == OPPONENT:
                r += 1
                c +=1
            if (r != row + 1 and c != col +1) and (r < 8 and c < 8) and self.board[r, c] == Board.EMPTY:
                legal_moves.append((r, c))
            
        if row <= 5 and col >= 2:   # diagonal from the cell towards bottom left
            r = row + 1
            c = col - 1
            while (r < 8 and c >= 0) and self.board[r, c] == OPPONENT:
                r += 1
                c -= 1
            if (r != row + 1 and c != col - 1) and (r < 8 and c >= 0) and self.board[r, c] == Board.EMPTY:
                legal_moves.append((r, c))


        return legal_moves

    def set_discs(self, row: int, col: int, PLAYER: int) -> None:
        '''Set the discs on the board as per the move made on the given cell'''
        self.board[row, col] = PLAYER
        OPPONENT = Board.WHITE if PLAYER == Board.BLACK else Board.BLACK

        # outflanking pieces on the right
        c = col + 1
        while c < 8 and self.board[row, c] == OPPONENT:
            c += 1
        if (c != col + 1 and c < 8) and self.board[row, c] == PLAYER: # outflanking is legal
            self.board[row, col:c] = PLAYER

        # outflanking pieces on the left
        c = col - 1
        while c >= 0 and self.board[row, c] == OPPONENT:
            c -= 1
        if (c != col - 1 and c >= 0) and self.board[row, c] == PLAYER:  # outflanking is ilegal
           self.board[row, c:col] = PLAYER

        # outflanking pieces below
        r = row + 1
        while r < 8 and self.board[r, col] == OPPONENT:
            r += 1
        if (r != row + 1 and r < 8) and self.board[r, col] == PLAYER:   # outflanking is legal
            self.board[row:r , col] = PLAYER

        # outflanking pieces above
        r = row - 1
        while r >= 0 and self.board[r, col] == OPPONENT:
            r -= 1
        if (r != row - 1 and r >= 0) and self.board[r, col] == PLAYER:   # outflanking is legal
            self.board[r:row, col] = PLAYER

        # outflanking pieces in the diagonal from the cell towards top left
        r = row - 1
        c = col - 1
        while (r >= 0 and c >= 0) and self.board[r, c] == OPPONENT:
            r -= 1
            c -= 1
        if (r != row - 1 and c != col - 1) and (r >= 0 and c >= 0) and self.board[r, c] == PLAYER:   # outflanking is legal
            r = row - 1
            c = col - 1
            while self.board[r, c] == OPPONENT:
                self.board[r, c] = PLAYER
                r -= 1
                c -= 1
            
        # outflanking pieces in the diagonal from the cell towards top right
        r = row - 1
        c = col + 1
        while (r >= 0 and c < 8) and self.board[r, c] == OPPONENT:
            r -= 1
            c += 1
        if (r != row - 1 and c != col + 1) and (r >= 0 and c < 8) and self.board[r, c] == PLAYER:   # outflanking is legal
            r = row - 1
            c = col + 1
            while self.board[r, c] == OPPONENT:
                self.board[r, c] = PLAYER
                r -= 1
                c += 1  

        # outflanking pieces in the diagonal from the cell towards bottom right
        r = row + 1
        c = col + 1
        while (r < 8 and c < 8) and self.board[r, c] == OPPONENT:
            r += 1
            c += 1
        if ( r != row + 1 and c != col + 1 ) and (r < 8 and c < 8) and self.board[r, c] == PLAYER:   # outflanking is legal
            r = row + 1
            c = col + 1
            while self.board[r, c] == OPPONENT:
                self.board[r, c] = PLAYER
                r += 1
                c += 1 

        # outflanking pieces in the diagonal from the cell towards bottom left
        r = row + 1
        c = col - 1
        while (r < 8 and c >= 0) and self.board[r, c] == OPPONENT:
            r += 1
            c -= 1
        if (r != row + 1 and c != col - 1) and (r < 8 and c >= 0) and self.board[r, c] == PLAYER:   # outflanking is legal
            r = row + 1
            c = col - 1
            while self.board[r, c] == OPPONENT:
                self.board[r, c] = PLAYER
                r += 1
                c -= 1
        
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