import random

from Code.agents.minimax_agent import MiniMaxAgent
from Code.game_logic.constants import CENTRAL_COLS, SEARCH_DEPTH


class RandomMiniMaxAgent(MiniMaxAgent):
    """
    This Agent is used to generate data for the ML-Agent.
    It works just as the normal MiniMaxAgent does, with the difference that there is
    a 20% chance that he chooses a random move (After checking for blocking or winning moves).
    """

    def choose_move(self, board):
        available_moves = board.get_available_moves()
        performance_move = self.performance_checks(board, available_moves)
        if  performance_move is not None:
            return performance_move

        else:
            """
            If the randomly generated number is 1, it returns a random move.
            Otherwise it just uses the minimax algorithm
            """
            random_chance = random.randint(0, 5)
            if random_chance == 1:
                return available_moves[random.randint(0, len(available_moves) - 1)]

            else:
                return self.minimax(board, SEARCH_DEPTH, True)[0]
