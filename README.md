# cs_1_connect4_ai
To use, download all these files and run Connect4.py in Python 2. To play against a Monte Carlo algorithm, type "monty" at the prompt, and to play against a minimax algorithm, type "minimax" at the prompt. Either the player or the computer will go first; it's random. To play, simply type the number of the column you want to put your piece into.

This simulates a Connect 4 game, and, notably, has an AI that plays using a minimax algorithm of adjustable depth with alpha-beta pruning that uses an adjustable number of Monte Carlo simulations at each endpoint in the resulting tree - however, it does not save this tree across each move of the game; implementing this would be a good way to markedly improve running speed.

As written, the minimax algorithm player won the first prize in the competition between such AIs in CS 1 2016 at Caltech and I'm pretty proud of that.

The runtime naturally varies based on machine. The default settings in the config file make it difficult to beat, but relatively slow to run on my computer.
