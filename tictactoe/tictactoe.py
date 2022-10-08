"""
Tic Tac Toe Player
"""

import copy
import math

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
    num_x = 0
    num_o = 0
    for i in board:
        for j in i:
            if j == X:
                num_x += 1
            if  i == O:
                num_o += 1
    
    if num_o == num_x:
        return X
    
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    
    return actions
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    if board[i][j] != EMPTY:
        raise Exception("The move is invalid, please check your move")

    board_copy = copy.deepcopy(board)

    turn = player(board_copy)

    board_copy[i][j] = turn

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        potential_winner = board[i][0]
        if potential_winner == board[i][1] and potential_winner == board[i][2]:
            return potential_winner
    
    for j in range(3):
        potential_winner = board[0][j]
        if potential_winner == board[1][j] and potential_winner == board[2][j]:
            return potential_winner

    potential_winner = board[1][1]
    if (potential_winner == board[0][0] and potential_winner == board[2][2]) or (potential_winner == board[0][2] and potential_winner == board[2][0]):
        return potential_winner

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is None:

        for i in board:
            for j in i:
                if j == EMPTY:
                    return False
                
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    potential_winner = winner(board)
    if potential_winner == X:
        return 1
    elif potential_winner == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if player(board) == X:
        optimal_score = -math.inf
        max_min_player = False
        
        for action in actions(board):
            new_board = result(board, action)
            new_score = minimax_algorithm(new_board, max_min_player)
            if new_score > optimal_score:
                optimal_score = new_score
                optimal_action = action
    
    else:
        optimal_score = math.inf
        max_min_player = True

        for action in actions(board):
            new_board = result(board, action)
            new_score = minimax_algorithm(new_board, max_min_player)
            if new_score < optimal_score:
                optimal_score = new_score
                optimal_action = action
    
    return optimal_action


    
def minimax_algorithm(board, max_min_player):
    if terminal(board):
        return utility(board)
    
    scores = []
    for action in actions(board):
        new_board = result(board, action)
        scores.append(minimax_algorithm(new_board, not max_min_player))

    if max_min_player:
        return max(scores) 
    else:
        return min(scores)