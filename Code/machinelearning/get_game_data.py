import numpy as np
from tqdm import tqdm

from Code.game_logic.constants import SYMBOL_PLAYER_TWO, SYMBOL_PLAYER_ONE, EMPTY
from Code.game_logic.game import turn_based_move, initialize_game


def flatten_board(gameboard):
    """
    Converts the string-based board into a numerical representation to transform and collect training data.
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


def record_games(num_games, player1, player2):
    """
    Records games between two players, but only saves moves made by player1.
    Used when the minimax-agent (player1) plays an agent which uses random moves (mostly SmartAgent) to record
    a variety of games and not play the same moves over and over again.


    :param num_games: number of games to record
    :param player1: The player whose moves we want to record (typically neural network)
    :param player2: The opponent player
    :return: Tuple of (X, y) where X are board states and y are moves by player1
    """
    data = []

    for _ in tqdm(range(num_games), desc="Simulating Games", unit="game"):
        turn, game_over, board = initialize_game()

        while not game_over:

            chosen_move, symbol, turn = turn_based_move(player1, player2, board, turn)

            # Only record when it's player1's turn
            if turn == 1:
                current_board_state = flatten_board(board)
                data.append((current_board_state, chosen_move))


            if board.is_full() or board.check_winner(symbol):
                game_over = True



    X = np.array([item[0] for item in data])
    y = np.array([item[1] for item in data])
    return X, y


def record_games_both_players(num_games,player1, player2):
    """
    Records a number of games between two players and collects it inside an array
    :param num_games: number of games to record
    :param player1: An instance of Player class
    :param player2: An instance of Player class
    :return: Tuple of (X, y) where X are board states and y are moves made by the players.
    """
    data = []

    for _ in tqdm(range(num_games), desc="Simulating Games", unit="game"):
        turn, game_over, board = initialize_game()
        while not game_over:
            chosen_move, symbol, turn = turn_based_move(player1, player2, board, turn)
            data.append((flatten_board(board), chosen_move))
            if board.is_full() or board.check_winner(symbol):
                game_over = True


    # Prepare machinelearning for training
    X = np.array([item[0] for item in data])  # Input features (flattened board states)
    y = np.array([item[1] for item in data])  # Labels (moves)

    return X, y

