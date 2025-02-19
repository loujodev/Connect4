from Code.Agents.player import Player
from Code.constants import DISTANCE_TO_BORDER, SCORE_TWO, SCORE_THREE, SCORE_WIN, SCORE_OPPONENT_CREATE_FOUR, \
    SCORE_OPPONENT_CREATE_THREE, SCORE_CENTRAL, SECTION_LENGTH, SCORE_BLOCK_OPPONENT_WIN, CENTRAL_ROW, CENTRAL_COLS, \
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
        Evaluates the position of a possible board state by using the given heuristics.

        :param board: the given board state
        :return score: the rated score of the board state
        """
        score = 0
        # Horizontally: Check the rows 3 and 4 symbols in a row
        for i in range(board.amount_rows):
            #Convert the i-th row to an array
            row_array = board.get_row(i)
            for col in range(board.amount_columns - DISTANCE_TO_BORDER):
                #Check sections(length 4) of 4 to search for a row of 3 or 4 identical symbols
                section = row_array[col:col+SECTION_LENGTH]
                if section.count(self.symbol) == 4:
                    score += SCORE_WIN
                elif section.count(self.symbol) == 3 and section.count(EMPTY) == 1:
                    score += SCORE_THREE


            # Vertically: Check the columns 3 and 4 symbols in a row
            for i in range(board.amount_columns):
                # Convert the i-th col to an array
                col_array = board.get_column(i)
                for row in range(board.amount_rows - DISTANCE_TO_BORDER):
                    if section.count(self.symbol) == 4:
                        score += SCORE_WIN
                    elif section.count(self.symbol) == 3 and section.count(EMPTY) == 1:
                        score += SCORE_THREE

            # Positve diagonally:
            for row in range(board.amount_rows - DISTANCE_TO_BORDER):
                for col in range(board.amount_columns - DISTANCE_TO_BORDER):
                    section = [board.board[row+i][col+i] for i in range(SECTION_LENGTH)]
                    if section.count(self.symbol) == 4:
                        score += SCORE_WIN
                    elif section.count(self.symbol) == 3 and section.count(EMPTY) == 1:
                        score += SCORE_THREE
            # Negative diagonally:
            for row in range(board.amount_rows - DISTANCE_TO_BORDER):
                for col in range(DISTANCE_TO_BORDER, board.amount_columns):
                    section = [board.board[row-i][col-i] for i in range(SECTION_LENGTH)]
                    if section.count(self.symbol) == 4:
                        score += SCORE_WIN
                    elif section.count(self.symbol) == 3 and section.count(EMPTY) == 1:
                        score += SCORE_THREE




            return score


    def choose_best_move(self, board):
        """
        Evaluates all possible moves and returns the best one by using the evaluate_position function.
        :param board:
        :return best_move: The best rated move by the MiniMax-Algorithm
        """
        available_moves = board.get_available_moves()
        best_move = -1
        best_score = 0

        # Simulate every playable move
        for move in available_moves:
            board.play_move(move, self.symbol)
            score = self.evaluate_position(board)

            #If the move is played in the central row or the central columns of the board the score is increased
            if move == CENTRAL_ROW:
                score += SCORE_CENTRAL
            if move in CENTRAL_COLS:
                score += SCORE_CENTRAL

            #Undo the move after the simulation
            board.undo_move(move,self.symbol)

            # If the simulated move results in a higher score than the current highest score, it becomes the best move
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

