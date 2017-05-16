final_players.py.old.old is compatible only with the version of Connect4.py included here. However, final_players.py and final_players.py.old are compatible with Connect4.py.old as well as the version of Connect4.py included here. All 3 are otherwise identical. That said, final_players.py.old.old has been tested extensively while the other 2 have not, although there are only minor differences between them, starting at line 449. If there's a weird problem with final_players.py, possibly with an AssertionError, maybe try replacing it with final_players.py.old or final_players.py.old.old first.

Neither version of final_players is compatible with the version of Connect4.py as originally given, as the original only contains options to play the four original players.

When playing Connect 4 vs. minimax, the depth of the search defaults to 6, and the number of simulations for the Monty cases defaults to 250. To change these values, change the values in minimax.config.

Connect4Sim.py simulates a user-entered number of games between monty and minimax with the starting values as given in the file.