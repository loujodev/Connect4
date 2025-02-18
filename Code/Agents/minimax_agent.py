from Code.Agents.player import Player
from Code.constants import DISTANCE_TO_BORDER, SCORE_TWO, SCORE_THREE, SCORE_WIN, SCORE_OPPONENT_TWO, \
    SCORE_OPPONENT_THREE, SCORE_CENTRAL, SECTION_LENGTH, SCORE_BLOCK_OPPONENT_WIN


class MiniMaxAgent(Player):
    """
    This Agent uses the MiniMax-Algorithm.

    The algorithm alternates between maximizing and minimizing the score while searching,
    assuming the opponent plays optimally as well.
    It tries to maximize the score for its own player and minimize the score for the opponent.
    At the end of the search, the best move will be chosen.

    It iterates over a tree of board states and uses the given heuristics to determine the best move.
    The heuristics can be adjusted in the constants.py file.

    The heuristics are:
    Winning move: +10000
    Central column: +4
    Two in a row: +2
    Three in a row: +5

    Creating a line of two for the opponent: -2
    Creating a line of three for the opponent: -100
    """



    def choose_move(self, board):
        return self.choose_best_move(board)

    def evaluate_position(self, board):
        score = 0
        # Check the horizontal rows 3 and 4 symbols in a row
        for i in range(board.amount_rows):
            #Convert the i-th row to an array
            row_array = [i for i in list(board[i,:])]
            for col in range(board.amount_columns - DISTANCE_TO_BORDER):
                #Check sections with a length of 4 to search for a row of 3 or 4 identical symbols
                section = row_array[col:col+SECTION_LENGTH]
                if section.count(self.symbol) == 4:
                    score += SCORE_WIN
                if section.count(self.symbol) == 3:
                    score += SCORE_THREE
                if section.count(self.opponent_symbol) == 3:
                    score += SCORE_BLOCK_OPPONENT_WIN



    def choose_best_move(self, board):
        available_moves = board.available_moves()
        best_move = -1
        best_score = 0

        # Simulate every playable move
        for move in available_moves:
            board.play_move(move, self.symbol)
            score = self.evaluate_position(board)
            board.undo_move(move)

            # If the simulated move results in a higher score than the current highest score, it becomes the best move
            if score > best_score:
                best_score = score
                best_move = move

