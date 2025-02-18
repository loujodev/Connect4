import random
from Code.Agents.player import Player


class RandomAgent(Player):

    def choose_move(self, board):
        """
        Returns a random valid column
        :param board: current game board
        :return col: random column index where a move can be made
        """
        col = col = random.randint(0, board.amount_columns - 1)
        while not board.valid_move(col):
            col = random.randint(0, board.amount_columns - 1)
        return col
