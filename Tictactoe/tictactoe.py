import math
from copy import deepcopy

# import sys


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
    # Returns player who has the next turn on a board.

    count_empty = 0
    count_X = 0
    count_O = 0

    for i in range(len(board)):
        count_empty += board[i].count(EMPTY)
        count_X += board[i].count(X)
        count_O += board[i].count(O)

    # We assume that player X always starts
    if count_empty == 9:
        return X
    elif count_X > count_O:
        return O
    elif count_O <= count_X:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    state = deepcopy(board)
    actions = set()

    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == None:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    state = deepcopy(board)

    if (0 > action[0] or action[0] > 2) or (
            0 > action[1] or action[1] > 2):  # Checks if the index is in the allowed scope
        raise IndexError
    elif state[action[0]][
        action[1]] is not None:  # Checks if the action (i,j) is assigned to an empty field
        raise Exception("action is not valid, board element already occupied")
    else:
        state[action[0]][action[1]] = player(state)
        return state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    state = board
    if (state[0][0] == "X") and (state[0][1] == "X") and (state[0][2] == "X"):  # horizontally check first row
        return X
    elif (state[0][0] == "O") and (state[0][1] == "O") and (state[0][2] == "O"):
        return O
    elif (state[1][0] == "X") and (state[1][1] == "X") and (state[1][2] == "X"):  # horizontally check second row
        return X
    elif (state[1][0] == "O") and (state[1][1] == "O") and (state[1][2] == "O"):
        return O
    elif (state[2][0] == "X") and (state[2][1] == "X") and (state[2][2] == "X"):  # horizontally check third row
        return X
    elif (state[2][0] == "O") and (state[2][1] == "O") and (state[2][2] == "O"):
        return O
    elif (state[0][0] == "X") and (state[1][0] == "X") and (state[2][0] == "X"):  # vertically check first col
        return X
    elif (state[0][0] == "O") and (state[1][0] == "O") and (state[2][0] == "O"):
        return O
    elif (state[0][1] == "X") and (state[1][1] == "X") and (state[2][1] == "X"):  # vertically check second col
        return X
    elif (state[0][1] == "O") and (state[1][1] == "O") and (state[2][1] == "O"):
        return O
    elif (state[0][2] == "X") and (state[1][2] == "X") and (state[2][2] == "X"):  # vertically check third col
        return X
    elif (state[0][2] == "O") and (state[1][2] == "O") and (state[2][2] == "O"):
        return O
    elif (state[0][0] == "X") and (state[1][1] == "X") and (
            state[2][2] == "X"):  # diagonally check from up-left to down-right
        return X
    elif (state[0][0] == "O") and (state[1][1] == "O") and (state[2][2] == "O"):
        return O
    elif (state[0][2] == "X") and (state[1][1] == "X") and (
            state[2][0] == "X"):  # diagonally check from up-right to down-left
        return X
    elif (state[0][2] == "O") and (state[1][1] == "O") and (
            state[2][0] == "O"):  # diagonally check from up-right to down-left
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    state = board
    if winner(board) == X or winner(board) == O:
        return True
    L = []
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == None:
                return False
            else:
                L.append(True)
    if all(L):
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == "X":
        max_value_list = []
        max_action_list = []

        for action in actions(board):
            max_action_list.append(action)
            value = min_value(result(board, action))
            max_value_list.append(value)

        for i in range(len(max_value_list)):
            if max(max_value_list) == max_value_list[i]:
                return max_action_list[i]
    else:
        min_value_list = []
        min_action_list = []

        for action in actions(board):
            min_action_list.append(action)
            value = max_value(result(board, action))
            min_value_list.append(value)

        for i in range(len(min_value_list)):
            if min(min_value_list) == min_value_list[i]:
                return min_action_list[i]


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
