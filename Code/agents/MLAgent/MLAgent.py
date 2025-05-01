import random

import numpy as np

from Code.agents.MLAgent.get_game_data import convert_board_to_cnn_input
from Code.agents.MLAgent.model import load_trained_model
from Code.agents.player import Player
from Code.environment.constants import AMOUNT_COLUMNS


class MlAgent(Player):
    """
    An agent that uses a pre-trained model to make decisions.
    The model used inside this project is a model that was trained by generating of the MiniMaxAgent(player1) playing against the SmartAgent.
    It is recommended to initialize the symbol property with  {SYMBOL_PLAYER_ONE} because this was the perspective
    on which he was trained on.
    """

    def __init__(self, symbol, opponent_symbol, model_path="connect4_cnn_model.keras"):
        """
        Initializes the Ml Agent with a given model
        It is recommended to initialize the symbol property with  {SYMBOL_PLAYER_ONE} because this was the perspective
        on which he was trained on.

        :param symbol: the symbol to play (SYMBOL_PLAYER_ONE strongly recommended)
        :param opponent_symbol: the symbol of his opponent (SYMBOL_PLAYER_ONE strongly recommended)
        :param model_path: the path to the trained model
        """
        super().__init__(symbol, opponent_symbol)
        self.model = load_trained_model(model_path)
        if self.model is None:
            raise ValueError(f"Could not load model from {model_path} ")
        print(f"ML Agent '{self.symbol}' initialized with model: {model_path}")

    def choose_move(self, board):
        """
        Chooses a move based on the current board state and the prediction made by the model.

        :param board: current board state
        :return int: An integer representing the chosen move.
        """
        available_moves = board.get_available_moves()

        if len(available_moves) == 1:
            return available_moves[0]

        try:

            cnn_input = convert_board_to_cnn_input(board, self.symbol)

            cnn_input_batch = np.expand_dims(cnn_input, axis=0)

            predictions = self.model.predict(cnn_input_batch, verbose=0)[0]

            masked_predictions = np.full(AMOUNT_COLUMNS, -np.inf)  # set values of unavailable moves  to -inf
            for move in available_moves:
                masked_predictions[move] = predictions[move]  # set values of available moves

            # choose the best move
            chosen_move = int(np.argmax(masked_predictions))

            return chosen_move



        except Exception as e:
            print(f"Error while predicting: {e}")
            print("Choosing a random move...")
            # Fallback
            return random.choice(available_moves)