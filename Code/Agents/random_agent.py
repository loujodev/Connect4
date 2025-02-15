from random import randrange
from Code.Agents.player import Player


class RandomAgent(Player):
    def choose_move(self, board):
        """
        Returns a random valid column
        :param board: current game board
        :return col: random column index where a move can be made
        """
        col = randrange(board.amount_columns)
        while not board.valid_move(col):
            col = randrange(board.amount_columns)
        return col
