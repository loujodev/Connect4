import random
import numpy as np
from Code.agents.player import Player
from Code.machinelearning.get_game_data import flatten_board


class NeuralNetworkPlayer(Player):
    def __init__(self, model, symbol, opponent_symbol, exploration_rate=0.1):
        super().__init__(symbol, opponent_symbol)
        self.model = model
        self.exploration_rate = exploration_rate  # For some randomness

    def choose_move(self, board):
        # Convert board to numerical representation
        board_state = flatten_board(board)

        # Add batch dimension and predict
        predictions = self.model.predict(board_state[np.newaxis, ...], verbose=0)[0]

        # Get valid moves (columns that aren't full)
        valid_moves = board.get_available_moves()

        # Filter predictions to only valid moves
        valid_predictions = [predictions[col] for col in valid_moves]

        # Exploration: sometimes choose random valid move
        if np.random.random() < self.exploration_rate:
            return random.choice(valid_moves)

        # Choose the best valid move according to model
        return valid_moves[np.argmax(valid_predictions)]