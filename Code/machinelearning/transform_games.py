import numpy as np
from Code.game_logic.constants import SYMBOL_PLAYER_TWO, SYMBOL_PLAYER_ONE, EMPTY


def flatten_board(gameboard):
    """
    Converts the string-based board into a numerical representation to collect training machinelearning.
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

def save_data(X, y, filename):
    """
    Saves the training machinelearning (X and y) to a .npz file.
    """
    np.savez(filename, X=X, y=y)
    print(f"Data saved to {filename}")

def load_data(filename):
    """
    Loads the training machinelearning (X and y) from a .npz file.
    """
    data = np.load(filename)
    X = data['X']
    y = data['y']
    print(f"Data loaded from {filename}")
    return X, y




