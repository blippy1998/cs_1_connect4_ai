# Name: Michael Rupprecht
# CMS cluster login name: mrupprec

'''
final_players.py

This module contains code for various bots that play Connect4 at varying 
degrees of sophistication.
'''

import random
from Connect4Simulator import *
# Any other imports go here...


class RandomPlayer:
    '''
    This player makes one of the possible moves on the game board,
    chosen at random.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''

        assert player in [1, 2]
        possibles = board.possibleMoves()
        assert possibles != []
        return random.choice(possibles)


class SimplePlayer:
    '''
    This player will always play a move that gives it a win if there is one.
    Otherwise, it picks a random legal move.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''
        
        moves = board.possibleMoves()

        assert moves != []

        # returns the first winning move it finds
        for move in moves:
            if board.isWinningMove(move, player):
                return move

        # if none exists, this line executes, returning a random move
        return random.choice(moves)


class BetterPlayer:
    '''
    This player will always play a move that gives it a win if there is one.
    Otherwise, it tries all moves, collects all the moves which don't allow
    the other player to win immediately, and picks one of those at random.
    If there is no such move, it picks a random move.
    '''

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''

        # makes 2 1 and 1 2
        player2 = player % 2 + 1
        moves = board.possibleMoves()

        assert moves != []

        # returns winning move, as before
        for move in moves:
            if board.isWinningMove(move, player):
                return move

        # winning move for the other player is the one to be blocked, and so
        # this returns that
        for move in moves:
            if board.isWinningMove(move, player2):
                return move

        # otherwise, random
        return random.choice(moves)

class Monty:
    '''
    This player will randomly simulate games for each possible move,
    picking the one that has the highest probability of success.
    '''

    def __init__(self, n, player, *move_list):
        '''
        Initialize the player using a simpler computer player.

        Arguments: 
          n      -- number of games to simulate.
          player -- the computer player
          move_list -- a list of possible moves that Monty is supposed to
          simulate. If not given, it will simulate all possible moves.
        '''

        assert n > 0
        self.player = player
        self.n = n
        if move_list:
            self.move_list = move_list[0]
        else:
            self.move_list = move_list

    def chooseMove(self, board, player):
        '''
        Given the current board and player number, choose and return a move.

        Arguments:
          board  -- a Connect4Board instance
          player -- either 1 or 2

        Precondition: There must be at least one legal move.
        Invariant: The board state does not change.
        '''

        # in this case, simulate all possible moves
        if not self.move_list:
            # makes 2 1 and 1 2
            player2 = player % 2 + 1
            moves = board.possibleMoves()

            assert moves != []

            # returns winning move, as before
            for move in moves:
                if board.isWinningMove(move, player):
                    return move

            # winning move for the other player is the one to be blocked, and so
            # this returns that
            for move in moves:
                if board.isWinningMove(move, player2):
                    return move

            # "dictionary of wins", or dwin
            # tracks how many wins each move gets in the simulation
            # this block counts wins per move and appends it to dwin
            dwin = {}
            for move in moves:
                wins = 0
                for i in range(self.n):
                    board2 = board.clone()
                    board2.makeMove(move, player)
                    c4s = Connect4Simulator(board2, BetterPlayer(),
                        BetterPlayer(), player2)
                    result = c4s.simulate()
                    if result == player:
                        wins += 1
                dwin[move] = wins

            ######################
            # print dwin
            ######################

            if not dwin:
                return random.choice(moves)

            max_wins = -1
            make_move = -1
            for entry in dwin.keys():
                if dwin[entry] > max_wins:
                    max_wins = dwin[entry]
                    make_move = entry
            return make_move

        player2 = player % 2 + 1

        ######################
        # print self.move_list
        ######################

        # otherwise, simulate only the moves in move_list
        moves = self.move_list

        # see above
        for move in moves:
            if board.isWinningMove(move, player):
                return move

        # see above
        for move in moves:
            if board.isWinningMove(move, player2):
                return move

        # see above
        dwin = {}
        for move in moves:
            wins = 0
            for i in range(self.n):
                board2 = board.clone()
                board2.makeMove(move, player)
                c4s = Connect4Simulator(board2, BetterPlayer(),
                    BetterPlayer(), player2)
                result = c4s.simulate()
                if result == player:
                    wins += 1
            dwin[move] = wins

        ######################
        # print dwin
        ######################

        # this avoids returning -1 if dwin is empty
        if not dwin:
            return random.choice(moves)

        max_wins = -1
        make_move = -1
        for entry in dwin.keys():

            # if dwin is all 0s, the stricty greater than allows the first move
            # to be selected
            if dwin[entry] > max_wins:
                max_wins = dwin[entry]
                make_move = entry
        return make_move

class Minimax:
    """
    Pretty much just wraps Tree and Node while contributing the chooseMove()
    method. It's neater this way.
    """

    class Tree:
        """
        This is pretty much the main part of the code here. It creates the tree,
        which consists of nodes, used for picking moves, using what I think is
        some sort of alpha-beta pruning algorithm.
        """

        class Node:
            """
            Node is the class used for each node of the tree. It is linked
            only downward, because the recursive subtree_maker() in the Tree
            class is what is used to go upward by one level each time.
            It represents a position on the Connect4Board, or, equivalently,
            a series of moves that leads up to that point.
            """

            def __init__(self):
                """
                Attributes:
                    subs: the list of child nodes
                    value: the value of whether a node leads to a win, loss, or
                    indeterminate. A win is 1, loss is -1, and indeterminate is
                    0.
                    move: each node represents a move made from the position of
                    the parent, so move denotes which move it is.
                """

                self.subs = []
                self.value = 0

                # temporary garbage value
                self.move = -1

            def getSubs(self):
                """Returns list of child nodes."""

                return self.subs

            def getValue(self):
                """Returns win/loss/indeterminate value of node."""

                return self.value

            def getMove(self):
                """Returns move value of node with respect to parent node."""

                return self.move

            def addSub(self, sub):
                """Appends a new child node to the list of child nodes."""

                self.subs.append(sub)

            def setValue(self, value):
                """Sets the win/loss/indeterminate value."""

                self.value = value

            def setMove(self, move):
                """Sets move value of node with respect to parent node."""

                self.move = move

        def __init__(self, board, player, depth):
            """
            Attributes:
                board: the Connect4Board on which it plays
                player: which player is to play
                depth: how many successive moves the tree should be made to
                represent.
                top: the top node of the tree
            """

            self.board = board
            self.player = player
            self.depth = depth

            self.top = self.Node()
            self.top.setMove(-1)

            # creates the entire tree recursively from the top node
            self.subtree_maker(self.board, self.top, self.player, self.depth)

        def subtree_maker(self, board, top, player, depth):
            """
            Makes the subtree of a node, and does it fast-ish using what I
            think is some form of alpha-beta pruning.
            Arguments:
                board: the current Connect4Board position
                top: the node being operated on - named "top" because the child
                nodes created will be below it.
                player: equivalent to "toMove" above.
                depth: how many levels to make the subtree.
            """

            moves = board.possibleMoves()

            # this forces Minimax to treat draws as losses
            # also conveniently fixes a nasty bug that causes searches where
            # Minimax runs out of moves to loop infinitely
            if moves == []:
                top.setValue(1)

            # if depth is 0, the building has completed, so it does nothing and
            # exits
            elif depth > 0:

                # for each move in the possible moves for the position at that
                # point (i.e. at that node)
                for move in moves:

                    node = self.Node()
                    node.setMove(move)
                    top.addSub(node)

                    # check if it's a winning move, in which case set top to -1
                    # because top is 1 level above node, so must be negative
                    # then break in order to stop generation of further nodes,
                    # because they'd be redundant; this saves time and might
                    # be some version of alpha-beta pruning
                    board2 = board.clone()
                    player2 = player % 2 + 1
                    win = False
                    if board2.isWinningMove(node.getMove(), player):
                        node.setValue(1)
                        top.setValue(-1)
                        win = True
                        break

                    # makes the move and creates the subtree of node using that
                    # "incremented" board, and a decremented depth so that the
                    # entire subtree will be the correct depth
                    board2.makeMove(node.getMove(), player)
                    self.subtree_maker(board2, node, player2, depth - 1)

                    # however, the *real* time-saver here is this bit; this part
                    # doesn't just break if node is a winning move, it breaks if
                    # node guarantees a win in the future
                    # it can tell at this point, because the subtree has already
                    # been made, so the final value of node has been determined
                    if node.getValue() == 1:
                        top.setValue(-1)
                        win = True
                        break

                # this sets the value of top if the other cases haven't been
                # satisfied; again negative because it's 1 level above
                if not win:
                    max_value = -board.getCols() - 1
                    for node in top.getSubs():
                        if node.getValue() > max_value:
                            max_value = node.getValue()

                    top.setValue(-max_value)

        def pprint_helper(self, top, tabs):
            """
            Allows pprint() to be a neat one line.
            Arguments:
                top: top node of the subtree to print
                tabs: how many tabs to print before the value (basically tells
                the depth of the top node)
            """

            # prints a series of tabs based on which depth the subtree is at
            # followed by the value at the node of the top of each subtree
            init_string = ""
            for i in range(tabs):
                init_string += "\t"
            print init_string + str(top.getValue())
            
            for node in top.getSubs():

                # if the node has any subs, it's not terminal, so
                # pprint_helper() continues on the node, incrementing the tab
                # because the subtree is one level deeper
                try:
                    node.getSubs()[0]
                    self.pprint_helper(node, tabs + 1)

                # otherwise, the node is terminal, so pprint_helper() exits and
                # "defers" to its calling function - either pprint_helper() or
                # pprint()
                except IndexError:
                    pass

        def pprint(self):
            """Pretty-prints the tree."""

            # prints the subtree of the top node starting with 0 tabs because
            # the first level is 0
            self.pprint_helper(self.top, 0)

        def move_table(self):
            """
            Returns the dictionary of win/loss/indeterminate values for each
            move from the top node of the tree.
            """

            result = {-1:[], 0:[], 1:[]}
            for node in self.top.getSubs():
                result[node.getValue()].append(node.getMove())
            return result

    def __init__(self, player, *depthmonty):
        """
        Initializes Minimax.
        Attributes:
            player: analogous to "toMove"
            depthmonty: optional input that should be of the form (depth, monty)
            if it is present, Minimax is created using the values specified
            below
            otherwise, it defaults to 5 for depth and 100 for monty
            depth: how deep to search (i.e. how many levels the tree should be)
            monty: how many simulations to run for indeterminate moves
        """

        assert player in [1, 2]
        self.player = player
        if depthmonty:
            assert len(depthmonty) == 2
            self.depth = depthmonty[0]
            self.monty = depthmonty[1]
        else:
            self.depth = 5
            self.monty = 100

    def chooseMove(self, board, player):
        """
        Chooses the move.
        Arguments:
            board: the current position on the Connect4Board
            player: analogous to "toMove"
        """

        moves = board.possibleMoves()
        assert moves != []

        #######

        # does the same thing as BetterPlayer so as to make or block a winning
        # move

        # makes 2 1 and 1 2
        player2 = player % 2 + 1

        # returns winning move, as before
        for move in moves:
            if board.isWinningMove(move, player):
                return move

        # winning move for the other player is the one to be blocked, and so
        # this returns that
        for move in moves:
            if board.isWinningMove(move, player2):
                return move

        #######

        # otherwise, makes a tree and selects the best move

        tree = self.Tree(board, player, self.depth)

        # tree.pprint()

        move_table = tree.move_table()

        ######################
        # print(move_table)
        ######################

        # if all the values in move_table are -1, the computer will lose against
        # a player who plays optimally, so it just chooses the first move
        # available
        if move_table[0] == [] and move_table[1] == []:
            return min(move_table[-1])

        # if the computer doesn't see a guaranteed winning move, it runs a Monty
        # simulation for each of the moves that aren't guaranteed losses
        # this is what uses the optional move_list argument in the Monty class
        if move_table[1] == []:
            monty = Monty(self.monty, player, move_table[0])
            return monty.chooseMove(board, player)

        # otherwise, the maximum value is 1, which means there is a winning move
        # in this case, return the first such move
        return min(move_table[1])