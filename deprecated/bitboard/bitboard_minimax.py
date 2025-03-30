from Code.agents.player import Player
from Code.game_logic.constants import DISTANCE_TO_BORDER, SCORE_TWO, SCORE_THREE, SCORE_WIN, \
    SCORE_CENTRAL, SECTION_LENGTH, SCORE_BLOCK_OPPONENT_WIN, CENTRAL_COLS, \
    SCORE_BLOCK_OPPONENT_THREE, AMOUNT_ROWS, AMOUNT_COLUMNS, BITBOARD_SEARCH_DEPTH
from deprecated.bitboard.bitboard import BitBoard  # Importiere die BitBoard-Klasse

class BitboardMiniMaxAgent(Player):
    """
    This Agent uses the MiniMax-Algorithm with BitBoard for efficient board representation.
    """
    def __init__(self, symbol, opponent_symbol):
        super().__init__(symbol, opponent_symbol)
        self.transposition_table = {}

    def choose_move(self, board):
        """
        Chooses the best move using the MiniMax algorithm with BitBoard.
        :param board: The current game board (GameBoard instance).
        :return: The best move (column index).
        """
        # Convert the GameBoard to a BitBoard
        bitboard = self.convert_to_bitboard(board)
        available_moves = bitboard.get_available_moves()

        # Check for a winning move, if one is found, the agent returns it
        winning_move = bitboard.get_winning_move(self.symbol, available_moves)
        if winning_move is not None:
            return winning_move

        #Check for a blocking move, if one is found, the agent returns it
        blocking_move = bitboard.get_winning_move(self.opponent_symbol, available_moves)
        if blocking_move is not None:
            return blocking_move

        if bitboard.is_empty():
            return CENTRAL_COLS[0]
        return self.minimax(bitboard, BITBOARD_SEARCH_DEPTH, True)[0]

    def convert_to_bitboard(self, game_board):
        """
        Converts a GameBoard instance to a BitBoard instance.
        :param game_board: The GameBoard instance to convert.
        :return: A BitBoard instance representing the same game state.
        """
        bitboard = BitBoard()
        bitboard.player1_board = bitboard.to_bitboards(self.symbol, game_board.board)
        bitboard.player2_board = bitboard.to_bitboards(self.opponent_symbol, game_board.board)
        return bitboard

    def evaluate_position(self, board):
        """
        Evaluates the current board state using BitBoard.
        :param board: The BitBoard instance representing the current game state.
        :return: The evaluated score.
        """
        score = 0

        # Evaluate central columns
        for col in CENTRAL_COLS:
            if (board.player1_board >> ((AMOUNT_ROWS - 1) * AMOUNT_COLUMNS + col)) & 1:
                score += SCORE_CENTRAL

        # Evaluate horizontal, vertical, and diagonal sections
        score += self.evaluate_sections(board.player1_board, board.player2_board)

        return score

    def evaluate_sections(self, player_board, opponent_board):
        """
        Evaluates all possible sections (horizontal, vertical, diagonal) for the given BitBoards.
        :param player_board: The BitBoard of the current player.
        :param opponent_board: The BitBoard of the opponent.
        :return: The evaluated score.
        """
        score = 0

        # Horizontal sections
        for row in range(AMOUNT_ROWS):
            for col in range(AMOUNT_COLUMNS - DISTANCE_TO_BORDER):
                section_mask = sum(1 << (row * AMOUNT_COLUMNS + col + i) for i in range(SECTION_LENGTH))
                score += self.evaluate_section(player_board, opponent_board, section_mask)

        # Vertical sections
        for col in range(AMOUNT_COLUMNS):
            for row in range(AMOUNT_ROWS - DISTANCE_TO_BORDER):
                section_mask = sum(1 << ((row + i) * AMOUNT_COLUMNS + col) for i in range(SECTION_LENGTH))
                score += self.evaluate_section(player_board, opponent_board, section_mask)

        # Diagonal sections (top-left to bottom-right)
        for row in range(AMOUNT_ROWS - DISTANCE_TO_BORDER):
            for col in range(AMOUNT_COLUMNS - DISTANCE_TO_BORDER):
                section_mask = sum(1 << ((row + i) * AMOUNT_COLUMNS + col + i) for i in range(SECTION_LENGTH))
                score += self.evaluate_section(player_board, opponent_board, section_mask)

        # Diagonal sections (bottom-left to top-right)
        for row in range(DISTANCE_TO_BORDER, AMOUNT_ROWS):
            for col in range(AMOUNT_COLUMNS - DISTANCE_TO_BORDER):
                section_mask = sum(1 << ((row - i) * AMOUNT_COLUMNS + col + i) for i in range(SECTION_LENGTH))
                score += self.evaluate_section(player_board, opponent_board, section_mask)

        return score

    def evaluate_section(self, player_board, opponent_board, section_mask):
        score = 0

        # Count player and opponent bits in the section
        player_count = bin(player_board & section_mask).count("1")
        opponent_count = bin(opponent_board & section_mask).count("1")
        empty_count = SECTION_LENGTH - player_count - opponent_count

        # Only evaluate player's potential win if opponent has no tokens in this section
        if opponent_count == 0:
            if player_count == SECTION_LENGTH:
                score += SCORE_WIN
            elif player_count == SECTION_LENGTH - 1 and empty_count == 1:
                score += SCORE_THREE
            elif player_count == SECTION_LENGTH - 2 and empty_count == 2:
                score += SCORE_TWO

        # Only evaluate blocking moves if player has no tokens in this section
        if player_count == 0:
            if opponent_count == SECTION_LENGTH - 1 and empty_count == 1:
                score += SCORE_BLOCK_OPPONENT_WIN
            elif opponent_count == SECTION_LENGTH - 2 and empty_count == 2:
                score += SCORE_BLOCK_OPPONENT_THREE

        return score

    def is_terminal(self, board):
        """
        Checks if a terminal state of the board is reached.
        :param board: The BitBoard instance representing the current game state.
        :return: True if the board is in a terminal state, False otherwise.
        """
        return board.is_full() or board.check_winner(self.symbol) or board.check_winner(self.opponent_symbol)


    def minimax(self, board, depth, maximizing, alpha=-float('inf'), beta=float('inf')):
        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                if board.check_winner(self.symbol):
                    return None, float('inf')
                elif board.check_winner(self.opponent_symbol):
                    return None, -float('inf')
            eval_score = self.evaluate_position(board)
            return None, eval_score

        available_moves = board.get_available_moves()

        best_move = available_moves[0]  # Default to first available move

        if maximizing:
            value = -float("inf")
            for move in available_moves:
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

        else:  # Minimizing
            value = float("inf")
            for move in available_moves:
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