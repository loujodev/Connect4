import random

import numpy as np
from tqdm import tqdm
import tensorflow as tf
from Code.environment.constants import SYMBOL_PLAYER_TWO, SYMBOL_PLAYER_ONE, EMPTY, AMOUNT_ROWS, AMOUNT_COLUMNS
from Code.environment.game import turn_based_move, initialize_game
"""
This file provides methods to record, transform, save and load game data to train the MlAgent.
"""

def convert_board_to_cnn_input(gameboard, player_symbol):
    """
    Converts the game board into a 3-channel representation for CNNs (6, 7, 3).
    Channels: 0=Empty, 1=Current Player's pieces, 2=Opponent's pieces.


    :param gameboard: The GameBoard object.
    :param player_symbol: The symbol of the player whose perspective is taken.


    :return np.ndarray: A NumPy array of shape (AMOUNT_ROWS, AMOUNT_COLUMNS, 3).
    """
    board = gameboard.board
    # Ensure dimensions from constants are correct
    cnn_board = np.zeros((AMOUNT_ROWS, AMOUNT_COLUMNS, 3), dtype=np.float32)

    opponent_symbol = SYMBOL_PLAYER_TWO if player_symbol == SYMBOL_PLAYER_ONE else SYMBOL_PLAYER_ONE

    for r in range(AMOUNT_ROWS):
        for c in range(AMOUNT_COLUMNS):
            if board[r][c] == EMPTY:
                cnn_board[r, c, 0] = 1.0
            elif board[r][c] == player_symbol:
                cnn_board[r, c, 1] = 1.0
            elif board[r][c] == opponent_symbol:
                cnn_board[r, c, 2] = 1.0
    return cnn_board


def save_data(X, y, filename):
    """
    Saves the training data (X) and one-hot encoded labels (y) to a .npz file.

    Args:
    :param X : The input features (board states).
    :param y : The one-hot encoded labels (moves).
    :param filename : The path to save the file.
    """
    np.savez(filename, X=X, y=y)
    print(f"Data saved to {filename}")


def load_data(filename):
    """
    Loads training data (X) and one-hot encoded labels (y) from a .npz file.


    :param filename: The path to the .npz file.


    :return tuple: (X, y)
        X (np.ndarray): The input features (board states).
        y (np.ndarray): The one-hot encoded labels (moves).
    """
    try:
        data = np.load(filename)
        X = data['X']
        y = data['y']
        print(f"Data loaded from {filename}")
        if len(y.shape) != 2 or y.shape[1] != AMOUNT_COLUMNS:
            print(
                f"Warning: Loaded 'y' data does not seem to be one-hot encoded (Shape: {y.shape}). Expected: (n_samples, {AMOUNT_COLUMNS})")
        return X, y
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return None, None
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return None, None


def record_games(num_games, player1, player2):
    """
    Records games, saving states and moves only from player1's perspective.
    Returns X (CNN input) and y (one-hot encoded moves).


    :param num_games: Number of games to simulate.
    :param player1: The player whose perspective and moves are recorded.
    :param player2: The opponent player.

    :return tuple: (X, y)
        X (np.ndarray): The input features (board states).
        y (np.ndarray): The one-hot encoded labels (moves).
    """
    data = []


    for _ in tqdm(range(num_games), desc=f"Simulating Games (Perspective {player1.symbol})", unit="game"):
        turn, game_over, board = initialize_game()
        board_history_player1 = []  # Stores (board_state_from_p1_view, move_p1)

        while not game_over:

            board_state_for_player1 = convert_board_to_cnn_input(board, player1.symbol)

            # Make the move
            chosen_move, symbol_played, turn = turn_based_move(player1, player2, board, turn)

            # If move was made by player 1 save it
            if symbol_played == player1.symbol:
                board_history_player1.append((board_state_for_player1, chosen_move))

            if board.is_full() or board.check_winner(symbol_played):
                game_over = True

        # Add the collected data from this game
        data.extend(board_history_player1)

    if not data:
        print("No data collected.")
        return None, None

    # Prepare data for training
    X = np.array([item[0] for item in data])
    y_indices = np.array([item[1] for item in data])

    # Convert y to one-hot encoding
    y_one_hot = tf.keras.utils.to_categorical(y_indices, num_classes=AMOUNT_COLUMNS)

    print(f"Recording finished. {len(data)} moves collected from Player 1.")
    print(f"X shape: {X.shape}, y_one_hot shape: {y_one_hot.shape}")
    return X, y_one_hot


def record_win_block_moves(num_games, player1, player2):
    """
    Records games, saving only (state, move) pairs where the move
    was either a winning move or blocked an opponent's winning move.
    The perspective is that of the player making the winning/blocking move.
    Returns X (CNN input) and y (one-hot moves).

    :param num_games: Number of games to simulate.
    :param player1: The player whose perspective and moves are recorded.
    :param player2: The opponent player.

    :return tuple: (X, y)
        X (np.ndarray): The input features (board states).
        y (np.ndarray): The one-hot encoded labels (moves).
    """
    data = []

    for _ in tqdm(range(num_games), desc="Simulating Games (Both Perspectives)", unit="game"):
        turn, game_over, board = initialize_game()

        while not game_over:
            current_player = player1 if turn == 0 else player2
            opponent_player = player1 if turn == 1 else player2
            player_symbol = current_player.symbol
            opponent_symbol = opponent_player.symbol
            available_moves = board.get_available_moves()

            winning_move = board.get_winning_move(player_symbol, available_moves)
            blocking_move = board.get_winning_move(opponent_symbol, available_moves)

            board_state_cnn = convert_board_to_cnn_input(board, player_symbol)

            # Make the move
            chosen_move, symbol_played, next_turn = turn_based_move(player1, player2, board, turn)

            if chosen_move == winning_move or chosen_move == blocking_move:
                data.append((board_state_cnn, chosen_move))

            turn = next_turn

            if board.is_full() or board.check_winner(symbol_played):
                game_over = True

    if not data:
        print("No data collected.")
        return None, None

    # Prepare data for training
    X = np.array([item[0] for item in data])
    y_indices = np.array([item[1] for item in data])

    # Convert y to one-hot encoding
    y_one_hot = tf.keras.utils.to_categorical(y_indices, num_classes=AMOUNT_COLUMNS)

    print(f"Recording finished. {len(data)} total moves collected.")
    print(f"X shape: {X.shape}, y_one_hot shape: {y_one_hot.shape}")
    return X, y_one_hot