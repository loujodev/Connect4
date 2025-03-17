from Code.agents.player import Player
from Code.constants import DISTANCE_TO_BORDER, SCORE_TWO, SCORE_THREE, SCORE_WIN, \
    SCORE_CENTRAL, SECTION_LENGTH, SCORE_BLOCK_OPPONENT_WIN, CENTRAL_COLS, \
    EMPTY, SCORE_BLOCK_OPPONENT_THREE, SEARCH_DEPTH, SCORE_FORK


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

    Creating a line of four for the opponent: -100
    Creating a line of three for the opponent: -2
    """


    def choose_move(self, board):
        available_moves = board.get_available_moves()

        # Check for a winning move, if one is found, the agent returns it
        winning_move = board.get_winning_move(self.symbol, available_moves)
        if winning_move is not None:
            return winning_move

        # Check for a blocking move, if one is found, the agent returns it
        blocking_move = board.get_winning_move(self.opponent_symbol, available_moves)
        if blocking_move is not None:
            return blocking_move



        if board.is_empty():
            return CENTRAL_COLS[0]

        return self.minimax(board, SEARCH_DEPTH, True)[0]

    def evaluate_position(self, move, board):
        """
        Evaluates the position of a possible board state by splitting the board
        into sections and evaluating them.

        :param move: the column in which a move was played
        :param board: the given board state after playing the move
        :return score: the rated score of the board state
        """
        score = 0

        ##If the move is played in the central columns of the board the score is increased
        if move in CENTRAL_COLS:
            score += SCORE_CENTRAL


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
        Evaluates a section of spaces(length determined by SECTION_LENGTH)  and checks for a winning condition, or multiple symbols inside a section.
        :param section: The section in the board (horizontally, vertically, or diagonally)
        :return: A score for the section
        """
        score = 0
        my_count = section.count(self.symbol)
        opp_count = section.count(self.opponent_symbol)
        empty_count = section.count(EMPTY)

        if my_count == SECTION_LENGTH:
            score += SCORE_WIN
        elif my_count == SECTION_LENGTH - 1 and empty_count == 1:
            score += SCORE_THREE
        elif my_count == SECTION_LENGTH - 2 and empty_count == 2:
            score += SCORE_TWO

        if opp_count == SECTION_LENGTH - 1 and empty_count == 1:
            score -= SCORE_BLOCK_OPPONENT_WIN
        elif opp_count == SECTION_LENGTH - 2 and empty_count == 2:
            score -= SCORE_BLOCK_OPPONENT_THREE

        return score



    def is_terminal(self, board):
        """
        Checks if a terminal state of the board is reached.
        This is the case is either the case if the board is full, or one of the player has won
        :param board: Current board state
        :return: True if the given board state is terminal, False otherwise
        """
        return board.is_full() or board.check_winner(self.symbol) or board.check_winner(self.opponent_symbol)



    def minimax(self, board, depth, maximizing, alpha=-float('inf'), beta=float('inf')):
        """
        Pseudocode source: https://en.wikipedia.org/wiki/Minimax

        Comments tbd
        :param board: A state of the board that should be evaluated
        :param depth: How deep the minimax algorithm should search
        :param maximizing: A boolean indicating whether to maximize or minimize
        :param alpha: Alpha parameter
        :param beta: Beta parameter
        :return: A score for the current board state while it has not searched to
        the end of the game tree or the board is not in the terminal state and a score

        """
        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                if board.check_winner(self.symbol):
                    return None, float('inf')
                elif board.check_winner(self.opponent_symbol):
                    return None, -float('inf')
            return None, self.evaluate_position(-1, board)

        best_move = board.get_available_moves()[0]  # Default to the first available move

        if maximizing:
            value = -float("inf")
            for move in board.get_available_moves():
                board.play_move(move, self.symbol)
                _, score = self.minimax(board, depth - 1, False, alpha, beta)
                board.undo_move(move, self.symbol)

                if score > value:
                    value = score
                    best_move = move

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return best_move, value

        else:  # minimizing
            value = float("inf")
            for move in board.get_available_moves():
                board.play_move(move, self.opponent_symbol)
                _, score = self.minimax(board, depth - 1, True, alpha, beta)
                board.undo_move(move, self.opponent_symbol)

                if score < value:
                    value = score
                    best_move = move

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return best_move, value

