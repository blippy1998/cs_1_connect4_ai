# Name: Michael Rupprecht
# CMS cluster login name: mrupprec

'''
final_board.py

This module contains classes that implement the Connect-4 board object.
'''

# Imports go here...
# about style: it seems the given code was in camelback, but I prefer
# underscore, so all of the variables that *I* defined are in the same style;
# I hope that's okay
# single letters usually either have relevant names (like c and r) or are
# typical, like i for a counter

class MoveError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    an invalid move is made.
    '''
    pass

class BoardError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    some erroneous condition relating to a Connect-Four board occurs.
    '''
    pass

class Connect4Board:
    '''
    Instance of this class manage a Connect-Four board, but do not
    manage the play of the game itself.
    '''

    def __init__(self):
        '''
        Initialize the board.
        '''

        # this might *technically* be brute force, but I used sublime's
        # ctrl+shift+L feature so it took me like 10 seconds to write out
        self.board = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]

        # self.board = [
        # [0, 0, 0],
        # [0, 0, 0],
        # [0, 0, 0],
        # [0, 0, 0]]

        self.cols = len(self.board)
        self.rows = len(self.board[0])

    def getRows(self):
        '''
        Return the number of rows.
        '''

        return self.rows

    def getCols(self):
        '''
        Return the number of columns.
        '''

        return self.cols

    def get(self, row, col):
        '''
        Arguments:
          row -- a valid row index
          col -- a valid column index

        Return value: the board value at (row, col).

        Raise a BoardError exception if the 'row' or 'col' value is invalid.
        '''

        error = "Invalid row or column number."
        if col < 0 or col >= self.getCols():
            raise BoardError(error)
        if row < 0 or row >= self.getRows():
            raise BoardError(error)

        try:
            return self.board[col][row]
        except IndexError:
            raise BoardError(error)

    def clone(self):
        '''
        Return a clone of this board i.e. a new instance of this class
        such that changing the fields of the new instance will not
        affect the old instance.

        Return value: the new Connect4Board instance.
        '''

        clonea = list()
        for a in self.board:
            clonea.append(list(a))
        clone = Connect4Board()
        clone.board = clonea
        clone.cols = len(self.board)
        clone.rows = len(self.board[0])
        return clone

    def possibleMoves(self):
        '''
        Compute the list of possible moves (i.e. a list of column numbers 
        corresponding to the columns which are not completely filled up).

        Return value: the list of possible moves
        '''

        moves = []
        num_cols = self.getCols()
        i = 0
        while i < num_cols:
            try:
                self.board[i].index(0)
                moves.append(i)
            except ValueError:
                pass
            i += 1
        return moves

    def makeMove(self, col, player):
        '''
        Make a move on the specified column for the specified player.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: none

        Raise a MoveError exception if a move cannot be made because the column
        is filled up, or if the column index or player number is invalid.
        '''

        if player != 1 and player != 2:
            raise MoveError("Invalid player number.")
        if col < 0:
            raise MoveError("Invalid column number.")
        try:
            row = self.board[col].index(0)
            self.board[col][row] = player
        except IndexError:
            raise MoveError("Invalid column number.")
        except ValueError:
            raise MoveError("The column is already filled.")

    def unmakeMove(self, col):
        '''
        Unmake the last move made on the specified column.

        Arguments:
          col -- a valid column index

        Return value: none

        Raise a MoveError exception if there is no move to unmake, or if the
        column index is invalid.
        '''

        if col < 0 or col >= self.getCols():
            raise MoveError("Invalid column number.")
        try:
            if self.board[col].index(0) == 0:
                raise MoveError("No moves have been made in this column.")
        except ValueError:
            pass

        # the try-except statement is to set the row value as the one below the
        # first one with a value of 0 (i.e. the first one that has a value of 1
        # or 2)
        # if this doesn't exist, it must be the top row
        try:
            row = self.board[col].index(0) - 1
        except ValueError:
            row = self.getRows() - 1
        self.board[col][row] = 0

    #
    ########
    ##################
    # isWin() and helper functions follow
    ##################
    ########
    #

    def isWin(self, col):
        '''
        Check to see if the last move played in column 'col' resulted in a win
        (four or more discs of the same color in a row in any direction).

        Argument: 
          col    -- a valid column index

        Return value: True if there is a win, else False

        Raise a BoardError exception if the column is empty (i.e. no move has
        ever been made in the column), or if the column index is invalid.
        '''

        if col < 0 or col >= self.getCols():
            raise BoardError("Invalid column number.")
        try:
            if self.board[col].index(0) == 0:
                raise BoardError("No moves have been made in this column.")
        except ValueError:
            pass

        if self.h_win(col) or self.v_win(col) or self.d_win(col):
            return True
        return False

    def d_win(self, col):
        """Checks for diagonal wins."""

        # sets bounds for the rows and columns it needs to check
        # it doesn't need to check any that are more than 3 away from it
        clow = col - 3
        chigh = col + 3
        try:
            row = self.board[col].index(0) - 1
        except ValueError:
            row = self.getRows() - 1
        rlow = row - 3
        rhigh = row + 3

        # increments each column and row up and right within the bounds and
        # checks how many consecutive pieces there are by comparing the value
        # of the current and the last piece; returns true if there are 4 in a
        # row
        consecutive_pieces = 1
        current_piece = -1
        last_piece = -1
        c = clow
        r = rlow
        while c <= chigh and r <= rhigh:
            try:
                if c < 0 or r < 0:
                    raise IndexError
                last_piece = current_piece
                current_piece = self.board[c][r]
                if last_piece == current_piece != 0:
                    consecutive_pieces += 1
                else:
                    consecutive_pieces = 1
                if consecutive_pieces >= 4:
                    return True
            except IndexError:
                pass
            c += 1
            r += 1

        # same thing, but increments up and left
        consecutive_pieces = 1
        current_piece = -1
        last_piece = -1
        c = chigh
        r = rlow
        while c >= clow and r <= rhigh:
            try:
                if c < 0 or r < 0:
                    raise IndexError
                last_piece = current_piece
                current_piece = self.board[c][r]
                if last_piece == current_piece != 0:
                    consecutive_pieces += 1
                else:
                    consecutive_pieces = 1
                if consecutive_pieces >= 4:
                    return True
            except IndexError:
                pass
            c -= 1
            r += 1

        # if nothing has been returned, there are not 4 in a row, so False is
        # returned
        return False

    def h_win(self, col):
        """Checks for horizontal wins."""

        # like d_win() but simpler, since it only has to check across

        # sets bounds
        low = max(col - 3, 0)
        high = min(col + 3, self.getCols() - 1)
        try:
            row = self.board[col].index(0) - 1
        except ValueError:
            row = self.getRows() - 1

        # analogous to d_win()
        consecutive_pieces = 1
        current_piece = -1
        last_piece = -1
        i = low
        while i <= high:
            last_piece = current_piece
            current_piece = self.board[i][row]
            if last_piece == current_piece != 0:
                consecutive_pieces += 1
            else:
                consecutive_pieces = 1
            if consecutive_pieces >= 4:
                return True
            i += 1
        return False

    def v_win(self, col):
        """Checks for vertical wins."""

        # sets bounds
        try:
            row = self.board[col].index(0) - 1
        except ValueError:
            row = self.getRows() - 1
        if row < 3:
            return False

        # only checks downward because an upward win is impossible
        current_piece = self.board[col][row]
        i = row - 1
        while i >= row - 3:
            if self.board[col][i] != current_piece:
                return False
            i -= 1
        return True

    #
    ########
    ##################
    # end of isWin() and helper functions
    ##################
    ########
    #

    def isDraw(self):
        '''
        Check to see if the board is a draw because there are no more
        columns to play in.

        Precondition: This assumes that there is no win on the board.

        Return value: True if there is a draw, else False
        '''

        for col in self.board:
            try:
                col.index(0)
                return False
            except ValueError:
                pass
        return True

    def isWinningMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a win.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a win, else False.

        Precondition: This assumes that the move can be made.
        '''

        board = self.clone()
        board.makeMove(col, player)
        return board.isWin(col)

    def isDrawingMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a draw.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a draw, else False.

        Precondition: This assumes that the move can be made, and that the
        move has been checked to see that it does not result in a win.
        '''

        board = self.clone()
        board.makeMove(col, player)
        return board.isDraw()

    # def makeTree(self, player):

    #     player2 = player % 2 + 1
    #     moves = self.possibleMoves()
    #     self.tree = []
    #     for move in moves:
    #         if move 
