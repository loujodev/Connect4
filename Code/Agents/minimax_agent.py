from Code.Agents.player import Player
from Code.constants import DISTANCE_TO_BORDER, SCORE_TWO, SCORE_THREE, SCORE_WIN, \
    SCORE_CENTRAL, SECTION_LENGTH, SCORE_BLOCK_OPPONENT_WIN, CENTRAL_ROWS, CENTRAL_COLS, \
    EMPTY


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

    Creating a line of three for the opponent: -2
    Creating a line of four for the opponent: -100
    """



    def choose_move(self, board):
        return self.choose_best_move(board)

    def evaluate_position(self, board):
        """
        Evaluates the position of a possible board state by splitting the board
        into sections and evaluating them.

        :param board: the given board state
        :return score: the rated score of the board state
        """
        score = 0

        # Horizontally: Check the rows for 3 or 4 symbols in a row
        for row in range(board.amount_rows):
            row_array = board.get_row(row)
            for col in range(board.amount_columns - DISTANCE_TO_BORDER):
                section = row_array[col:col + SECTION_LENGTH]
                score += self.evaluate_section(section)

        # Vertically: Check the columns for 3 or 4 symbols in a row
        for col in range(board.amount_columns):
            col_array = board.get_column(col)
            for row in range(board.amount_rows - DISTANCE_TO_BORDER):
                section = col_array[row:row + SECTION_LENGTH]
                score += self.evaluate_section(section)

        # Positive diagonally: Check for 3 or 4 symbols in a row
        for row in range(board.amount_rows - DISTANCE_TO_BORDER):
            for col in range(board.amount_columns - DISTANCE_TO_BORDER):
                section = [board.board[row + i][col + i] for i in range(SECTION_LENGTH)]
                score += self.evaluate_section(section)

        # Negative diagonally: Check for 3 or 4 symbols in a row
        for row in range(board.amount_rows - DISTANCE_TO_BORDER):
            for col in range(board.amount_columns - DISTANCE_TO_BORDER):
                section = [board.board[row + DISTANCE_TO_BORDER - i][col + i] for i in range(SECTION_LENGTH)]
                score += self.evaluate_section(section)

        return score

    def evaluate_section(self, section):
        """
        Evaluates a section of four spaces and checks for a winning condition, 3 symbols and an empty space or 2 symbols
        and an empty space.

        :param section: A section of four spaces in the board (horizontally, vertically, or diagonally)
        :param symbol: The symbol of the player to evaluate the section for
        :return: A score for the section
        """
        score = 0
        if section.count(self.symbol) == 4:
            score += SCORE_WIN
            "Winning move found!"
        elif section.count(self.symbol) == 3 and section.count(EMPTY) == 1:
            "3 Three in a row found!"
            score += SCORE_THREE
        elif section.count(self.symbol) == 2 and section.count(EMPTY) == 2:
            score += SCORE_TWO

        # Check for opponent's potential winning moves
        if section.count(self.opponent_symbol) == 3 and section.count(EMPTY) == 1:
            "3 Three in a row for oponnent found!"
            score -= SCORE_BLOCK_OPPONENT_WIN  # High priority to block opponent's winning move

        return score





    def choose_best_move(self, board):
        """
        Evaluates all possible moves and returns the best one by using the evaluate_position function.
        :param board:
        :return best_move: The best rated move by the MiniMax-Algorithm
        """
        available_moves = board.get_available_moves()
        best_move  = available_moves[0]
        best_score = -100000000000

        # Simulate every playable move
        for move in available_moves:
            board.play_move(move, self.symbol)
            score = self.evaluate_position(board)

            ##If the move is played in the central columns of the board the score is increased
            if move in CENTRAL_COLS:
                score += SCORE_CENTRAL
            if move in CENTRAL_ROWS:
                score += SCORE_CENTRAL

            #Undo the move after the simulation
            board.undo_move(move,self.symbol)

            print(f"move: {move}, score: {score}")
            # If the simulated move results in a higher score than the current highest score, it becomes the best move
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

