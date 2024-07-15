import numpy as np
import contextlib
# board = np.random.randint(10, size=(3,3))
# print(board)
# print(board[2][:])
# print(np.array([board[i][0] for i in range(len(board[:][0]))]))

# board = [[None]*3,[None]*3,[None]*3]

# print(any(None in row for row in board))

# board = [[None]*4 for i in range(8)]
# board = [(1,2),(3,4)]
# board.append([])
# board = [i for i in board if i != []]

board = [3,2]
board1 = (3,2)
# board.append([5,6])
# board = [one + two for one,two in zip(board,board1)]

print(board == board1)