import random

import numpy as np

from Code.agents.MLAgent.model import load_trained_model
from Code.agents.player import Player
from Code.environment.constants import AMOUNT_COLUMNS
from Code.agents.MLAgent.get_game_data import convert_board_to_cnn_input


class MlAgent(Player):
    """
    Ein Agent, der ein trainiertes Keras CNN-Modell verwendet, um Züge auszuwählen.
    """
    def __init__(self, symbol, opponent_symbol, model_path="connect4_cnn_model.keras"):
        """
        Initialisiert den ML-Agenten.

        Args:
            symbol (str): Das Symbol des Agenten.
            opponent_symbol (str): Das Symbol des Gegners.
            model_path (str): Der Pfad zur gespeicherten Modelldatei (.keras).
        """
        super().__init__(symbol, opponent_symbol)
        self.model = load_trained_model(model_path)
        if self.model is None:
            raise ValueError(f"Could not load model from {model_path} ")
        print(f"ML Agent '{self.symbol}' initialized with model: {model_path}")

    def choose_move(self, board):
        """
        Wählt einen Zug basierend auf der Vorhersage des CNN-Modells.

        Args:
            board (GameBoard): Das aktuelle Spielbrett-Objekt.

        Returns:
            int: Der Index der Spalte für den nächsten Zug.
                 Gibt einen zufälligen validen Zug zurück, wenn keine Vorhersage möglich ist.
        """
        available_moves = board.get_available_moves()

        if len(available_moves) == 1:
            return available_moves[0]

        try:

            cnn_input = convert_board_to_cnn_input(board, self.symbol)


            cnn_input_batch = np.expand_dims(cnn_input, axis=0)

            predictions = self.model.predict(cnn_input_batch)[0]

            masked_predictions = np.full(AMOUNT_COLUMNS, -np.inf) #set values of unavailable moves  to -inf
            for move in available_moves:
                 masked_predictions[move] = predictions[move]  #set values of available moves

            # choose the best move
            chosen_move = int(np.argmax(masked_predictions))


            return chosen_move



        except Exception as e:
            print(f"Error while predicting: {e}")
            print("Choosing a random move...")
            # Fallback
            return random.choice(available_moves)