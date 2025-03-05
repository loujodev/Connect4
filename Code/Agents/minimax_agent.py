from Code.Agents.player import Player
from Code.constants import DISTANCE_TO_BORDER, SCORE_TWO, SCORE_THREE, SCORE_WIN, \
    SCORE_CENTRAL, SECTION_LENGTH, SCORE_BLOCK_OPPONENT_WIN, CENTRAL_COLS, \
    EMPTY, SCORE_BLOCK_OPPONENT_THREE, SEARCH_DEPTH


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
        if board.is_empty():
            return CENTRAL_COLS[0]
        return self.minimax(board,SEARCH_DEPTH, True)[0]

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
        Evaluates a section of four spaces and checks for a winning condition, 3 symbols and an empty space or 2 symbols
        and an empty space.

        :param section: A section of four spaces in the board (horizontally, vertically, or diagonally)
        :param symbol: The symbol of the player to evaluate the section for
        :return: A score for the section
        """
        score = 0
        if section.count(self.symbol) == SECTION_LENGTH:
            score += SCORE_WIN
            "Winning move found!"
        elif section.count(self.symbol) == SECTION_LENGTH-1 and section.count(EMPTY) == 1:
            score += SCORE_THREE
        elif section.count(self.symbol) == SECTION_LENGTH-2 and section.count(EMPTY) == 2:
            score += SCORE_TWO

        # Check for opponent's potential winning moves
        if section.count(self.opponent_symbol) == SECTION_LENGTH-1 and section.count(EMPTY) == 1:
            score -= SCORE_BLOCK_OPPONENT_WIN
        elif section.count(self.opponent_symbol) == SECTION_LENGTH-2 and section.count(EMPTY) == 2:
            score -= SCORE_BLOCK_OPPONENT_THREE

        return score


    def choose_best_move(self, board):
        """
            Evaluates all possible moves and returns the best one by using the evaluate_position function.
            :param board: current board state
            :return best_move: The best rated move by the MiniMax-Algorithm
            """
        available_moves = board.get_available_moves()
        best_move = available_moves[0]
        best_score = -float('-inf')

        # Simulate every playable move
        for move in available_moves:
            board.play_move(move, self.symbol)
            score = self.evaluate_position(move, board)

            # Undo the move after the simulation
            board.undo_move(move, self.symbol)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

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
                _, score = self.minimax(board, depth - 1, False, alpha, beta)  # Alternate to minimizing
                board.undo_move(move, self.symbol)

                if score > value:
                    value = score
                    best_move = move

                alpha = max(alpha, value)  # Update alpha
                if alpha >= beta:
                    break  # Beta cutoff

            return best_move, value

        else:  # minimizing
            value = float("inf")
            for move in board.get_available_moves():
                board.play_move(move, self.opponent_symbol)  # Play the opponent's symbol
                _, score = self.minimax(board, depth - 1, True, alpha, beta)  # Alternate to maximizing
                board.undo_move(move, self.opponent_symbol)

                if score < value:
                    value = score
                    best_move = move

                beta = min(beta, value)  # Update beta
                if alpha >= beta:
                    break  # Alpha cutoff

            return best_move, value