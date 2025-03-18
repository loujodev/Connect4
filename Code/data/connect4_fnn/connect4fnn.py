import numpy as np

from Code.game_logic.constants import SYMBOL_PLAYER_TWO, SYMBOL_PLAYER_ONE, EMPTY


def flatten_board(gameboard):
    """
    Converts the string-based board into a numerical representation to collect training data.
    """
    board = gameboard.board
    numerical_board = []
    for row in board:
        numerical_row = []
        for cell in row:
            if cell == EMPTY:
                numerical_row.append(0)
            elif cell == SYMBOL_PLAYER_ONE:
                numerical_row.append(1)
            elif cell == SYMBOL_PLAYER_TWO:
                numerical_row.append(-1)
        numerical_board.append(numerical_row)
    #Convert the board to a numpy array and flatten it to a 1D Vector
    return np.array(numerical_board, dtype=np.float32).flatten()

def collect_game_data():
    pass

