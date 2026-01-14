#N-dimenisonal N-player tic tac toe:

import numpy as np

num_players = input("How many players?\n")
if not num_players.isdigit() or int(num_players) <= 1:
    raise ValueError("Number of Players must be an integer greater than 1")
num_players = int(num_players)

def iswon(game):
    pass

board = np.zeros((3,)*num_players)
order={k: np.argsort([k]+[i for i in range(num_players) if i != k]) for k in range(num_players)}

turn = 0
while not iswon(board):
    print(f"\n----\nPlayer {turn}'s turn")
    print(order[turn])
    print(board[order[turn]])
    pmove = input(f"Select a board to play on (0-3) or type 'board' to see the full board:\n")
    
    if pmove == 'board':
        print(board)
    elif not pmove.isnumeric() or int(pmove) not in range(0, 2):
        print("Invalid Input")
        continue
    turn +=1
    turn = turn % num_players
