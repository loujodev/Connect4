import random
from Code.agents.player import Player


class RandomAgent(Player):

    def choose_move(self, board):
        """
        Returns a random valid column
        :param board: current game board
        :return col: random column index where a move can be made
        """
        available_moves = board.get_available_moves()


        return available_moves[random.randint(0, len(available_moves) - 1)]
