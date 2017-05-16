import sys
from final_board import *
from final_players import *
import random

class Connect4Sim:
    '''Instances of this class simulate an interactive Connect-4 game.'''

    def __init__(self, player1, opponent, toMove):
        '''
        Initializes the game.

        Arguments:
          opponent -- the computer opponent object
          toMove   -- the first player to move.  1 = human, 2 = computer.
        '''
        assert toMove in [1, 2]
        self.toMove = toMove
        self.player1 = player1
        self.opponent = opponent
        self.board = Connect4Board()
        self.nrows = self.board.getRows()
        self.ncols = self.board.getCols()
        self.moves = []

    def show(self):
        '''Print the board to the terminal, along with the player to move.'''

        print
        print '     top'
        print '-------------'
        for row in range(self.nrows-1, -1, -1):
            for col in range(0, self.ncols):
                val = self.board.get(row, col)
                if val == 0:
                    print '.',
                else:
                    print val,
            print
        print '-------------'
        print '0 1 2 3 4 5 6'
        print '   column'
        print

    def makeMove(self, col, player):
        '''
        Make a move on the board.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2
        '''

        if col < 0 or col >= self.ncols:
            raise MoveError('invalid move: %d' % col)
        self.board.makeMove(col, player)
        self.moves.append((player, col))

    def unmakeMove(self):
        '''
        Unmake a move on the board.  This means that the last move by
        both players is undone i.e. those locations on the board are cleared.

        Raise a MoveError exception if there are not enough moves to undo.
        '''

        if len(self.moves) > 1:
            self.board.unmakeMove(self.moves.pop()[1])
            self.board.unmakeMove(self.moves.pop()[1])
        else:
            raise MoveError('Not enough moves to undo!')

    def changePlayerToMove(self):
        '''Change the player to move.'''

        self.toMove = 3 - self.toMove   # changes 2 -> 1 and 1 -> 2

    def play(self):
        '''
        Play a game of Connect-4 interactively against the computer opponent.
        Stop if either player wins or if the board is full.  Allow the user to
        undo moves.
        '''

        # game.show()
        # print 'Player %d to move.\n' % self.toMove

        while True:
            try:
                if self.toMove == 1:  # player 1 = human
                    col = self.player1.chooseMove(self.board.clone(), 1)
                    self.makeMove(col, 1)
                    # print 'SimplePlayer plays on column %d...' % col
                    # self.show()
                else:  # player 2 = computer
                    col = self.opponent.chooseMove(self.board.clone(), 2)
                    self.makeMove(col, 2)
                    # print 'Minimax plays on column %d...' % col
                    # self.show()

                # Check for wins or draws.
                if self.board.isWin(col):
                    # print "Game over: player %d wins!" % self.toMove
                    return self.toMove

                if self.board.isDraw():
                    # print "Game over: the game is a draw."
                    return 0

                self.changePlayerToMove()
                # print 'Player %d to move.\n' % self.toMove

            except ValueError, e:
                print e
                print >> sys.stderr, 'Invalid command; try again...'

            except MoveError, e:
                print e
                print >> sys.stderr, 'Move error; try again...'

            except BoardError, e:
                print e
                print >> sys.stderr, 'Board error; try again...'

if __name__ == '__main__':
    # depth = int(raw_input("Enter depth to search " + \
    #     "for the minimax algorithm: "))
    # assert depth > 0
    # opponent = Minimax(1, depth)
    opponent = Monty(100, 2)
    player1 = Minimax(1, 5, 100)

    n = int(raw_input("Enter number of simulations: "))

    simple = 0
    minimax = 0
    draw = 0
    for i in range(n):
        print i
        toMove = random.choice([1, 2])
        # print
        # print 'First player to move: %d' % toMove
        # print
        game = Connect4Sim(player1, opponent, toMove)
        result = game.play()
        if result == 2:
            simple += 1
        elif result == 1:
            minimax += 1
        else:
            draw += 1
    print simple, minimax, draw