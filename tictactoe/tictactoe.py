"""
Tic Tac Toe Player
"""

import math, copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # print(f"entered player")

    # if terminal board is input, then any value can be returned
    if terminal(board) == True:
        return X
    
    flat_board = [element for sublist in board for element in sublist]

    # X gets the first move
    if flat_board.count(EMPTY) == 9:
        return X

    # alternate: if number of "O" is par, then "O" turn 
    if (flat_board.count(X) > flat_board.count(O)):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # print(f"entered actions")

    # if terminal board is input, then any value can be returned
    if terminal(board) == True:
        return X
    
    # i corresponds to row of move, j corresponds to cell in the row
    # moves are any cells on board not with an X or 0 in them
    moves = set()
    for i in range(len(board)):  # Iterate over rows
        for j in range(len(board[i])):  # Iterate over columns
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # print(f"entered result")
    
    # if action is None or not tuple, raise exception
    if action == None or type(action) != tuple:
        raise Exception(f"can't input {action}, empty or invalid action")

    # if action outside walls, raise exception
    if (action[0]>2 or action [1]>2) or (action[0]<0 or action[1]<0):
        raise Exception("can't play outside walls")

    # there's already a move there
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("there's already a move there")
    
    # return new board as list
        # make deep copy of board first, since it will require considering many board states
        # there's something more to this "deep copy part"
    copy_board = copy.deepcopy(board)
    
    copy_board[action[0]][action[1]] = player(copy_board)

    return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # print(f"entered winner")

    # return winner of board if there's one, assume there's only one winner at most        
    
    # check for horizontals
    for i in range(0,3):
        if board[i].count(X) == 3: return X
        if board[i].count(O) == 3: return O

    # check for verticals
        count_X_vertical = 0
        count_O_vertical = 0
        for row in range(0,3):
            if board[row][i] == X: count_X_vertical+=1
            if board[row][i] == O: count_O_vertical+=1

        if count_X_vertical == 3: return X
        if count_O_vertical == 3: return O

    # check for simple diagonals by counting X or O in diagonal
    num_X_simple_diag = 0
    num_O_simple_diag = 0
    for i in range(0,3):
        # count X
        # count O
        # if X or O == 3 then return
        if board[i][i] == X: num_X_simple_diag += 1
        if board[i][i] == O: num_O_simple_diag += 1
    
    if num_X_simple_diag == 3: return X
    if num_O_simple_diag == 3: return O     

    # check for opposite diagonals by counting X or O in diagonal
    num_X_opposite_diag = 0
    num_O_opposite_diag = 0
    for i in range(0,3):
        # count X
        # count O
        # if X or O == 3 then return
        if board[i][2-i] == X: num_X_opposite_diag += 1
        if board[i][2-i] == O: num_O_opposite_diag += 1
    
    if num_X_opposite_diag == 3:
        return X
    if num_O_opposite_diag == 3:
            return O     
    
    # return None if there's no winner
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # return True if somebody won or all cells full
        # check if there's winner
        # check if all cells full
    # return False if game is in progress
    flat_board = [element for sublist in board for element in sublist]
    if winner(board) != None or flat_board.count(EMPTY) == 0:
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    # print(f"entered utility")
    # receives a TERMINAL board as input
        # return utility of board
        # assume utility is only called when terminal(board) == True
    if winner(board) == X: return 1
    else:
        if winner(board) == O: return -1
        else: return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # PSEUDOCODE
    # returns optimal move for the next player (i,j)
        # if multiple moves are optimal, then any is acceptable
    # if board is terminal then return None
    if terminal(board) == True:
        return None
    
    if player(board) == X:
        max_value = Max_Value(board)[1]
        return max_value
    if player(board) == O:
        min_value = Min_Value(board)[1]
        return min_value

def Min_Value(board):
    v = float('inf')
    action_min = None
    max_function = ()
    if terminal(board) == True:
        return (utility(board),None)
    for action in actions(board):
        max_function = Max_Value(result(board,action))
        if max_function[0] < v:
            action_min = action
            v = max_function[0]
    return (v,action_min) 

def Max_Value(board):
    v = float('-inf')
    action_max = None
    min_function = ()
    if terminal(board) == True:
        return (utility(board),None)
    for action in actions(board):
        min_function = Min_Value(result(board,action))
        if min_function[0] > v:
            action_max = action
            v = min_function[0]
    return (v,action_max)