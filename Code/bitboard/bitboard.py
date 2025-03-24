from Code.game_logic.constants import DISTANCE_TO_BORDER, EMPTY, SECTION_LENGTH, AMOUNT_ROWS, AMOUNT_COLUMNS, \
    SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO


class BitBoard:
    def __init__(self):
        """
        Initializes an empty board with given amount of column and rows.
        """
        self.amount_columns = AMOUNT_COLUMNS
        self.amount_rows = AMOUNT_ROWS
        self.player1_board = 0  # Bitboard for the current player
        self.player2_board = 0  # Bitboard for the opponent

    def get_combined_board(self):
        """
        Returns the combined bitboard representing the entire game state.
        :return: The combined bitboard.
        """
        return self.player1_board | self.player2_board

    def to_bitboards(self, player_symbol, board):


        bitboard = 0  # Start with an empty bitboard
        bit_position = 0  # Tracks the current bit position

        # Loop through the board from bottom to top and left to right
        for row in reversed(range(self.amount_rows)):
            for col in range(self.amount_columns):
                if board[row][col] == player_symbol:
                    # Sets the bit at bit_position to 1
                    bitboard |= 1 << bit_position
                bit_position += 1

        return bitboard

    def get_row(self, row_index):
        """
        Returns the row at the given index from the combined bitboard.
        :param row_index: The index of the row to retrieve.
        :return: A list representing the row.
        """
        combined_board = self.get_combined_board()
        row = []
        for col in range(self.amount_columns):
            bit_position = row_index * self.amount_columns + col
            row.append((combined_board >> bit_position) & 1)
        return row

    def get_column(self, col_index):
        """
        Returns the column at the given index from the combined bitboard.
        :param col_index: The index of the column to retrieve.
        :return: A list representing the column.
        """
        combined_board = self.get_combined_board()
        column = []
        for row in range(self.amount_rows):
            bit_position = row * self.amount_columns + col_index
            column.append((combined_board >> bit_position) & 1)
        return column

    def print_board(self):
        """
        Iterates over the board and prints each row with a line underneath.
        """
        print("------------------------------")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for row in reversed(range(self.amount_rows)):
            row_str = []
            for col in range(self.amount_columns):
                bit_position = row * self.amount_columns + col
                if (self.player1_board >> bit_position) & 1:
                    row_str.append("X")
                elif (self.player2_board >> bit_position) & 1:
                    row_str.append("O")
                else:
                    row_str.append(" ")
            print("  ┃  ".join(row_str))
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    def is_full(self):
        """
        Checks if the board is full.
        :return: True if the board is full, False otherwise.
        """
        combined_board = self.get_combined_board()
        mask = (1 << (self.amount_columns * self.amount_rows)) - 1
        return (combined_board & mask) == mask

    def is_empty(self):
        """
        Checks if the board is empty.
        :return: True if the board is empty, False otherwise.
        """
        return self.player1_board == 0 and self.player2_board == 0

    def valid_move(self, column):
        """
        Checks if the given column results in a valid move.
        :param column: The column index to check for a valid move.
        :return: True if the column is valid, False otherwise.
        """
        if isinstance(column, int) and self.amount_columns > column >= 0:
            top_row_bit_position = (self.amount_rows - 1) * self.amount_columns + column
            return not ((self.get_combined_board() >> top_row_bit_position) & 1)
        return False

    def get_available_moves(self):
        """
        Determine the list of available moves for the current board state.
        :return: A list of integers representing the columns where moves are valid.
        """
        available_moves = []
        for col in range(self.amount_columns):
            if self.valid_move(col):
                available_moves.append(col)
        return available_moves

    def play_move(self, column, symbol):
        """
        Handles the placement of a player's symbol in the chosen column for a move in the game.
        :param column: The column index where the move is played.
        :param symbol: The symbol to place in the chosen column.
        """
        for row in range(self.amount_rows):
            bit_position = row * self.amount_columns + column
            if not ((self.get_combined_board() >> bit_position) & 1):
                if symbol == SYMBOL_PLAYER_ONE:
                    self.player1_board |= 1 << bit_position
                else:
                    self.player2_board |= 1 << bit_position
                break

    def check_winner(self, symbol):
        """
        Checks if there is a winner for the given symbol.
        :param symbol: The symbol to check for a win.
        :return: True if a winner is found, False otherwise.
        """
        # Determine which bitboard to check based on the symbol
        bitboard = self.player1_board if symbol == SYMBOL_PLAYER_ONE else self.player2_board

        # Check horizontally
        for row in range(self.amount_rows):
            for col in range(self.amount_columns - DISTANCE_TO_BORDER):
                if all((bitboard >> (row * self.amount_columns + col + i)) & 1 for i in range(SECTION_LENGTH)):
                    return True

        # Check vertically
        for col in range(self.amount_columns):
            for row in range(self.amount_rows - DISTANCE_TO_BORDER):
                if all((bitboard >> ((row + i) * self.amount_columns + col)) & 1 for i in range(SECTION_LENGTH)):
                    return True

        # Check diagonally (top-left to bottom-right)
        for row in range(self.amount_rows - DISTANCE_TO_BORDER):
            for col in range(self.amount_columns - DISTANCE_TO_BORDER):
                if all((bitboard >> ((row + i) * self.amount_columns + col + i)) & 1 for i in range(SECTION_LENGTH)):
                    return True

        # Check diagonally (bottom-left to top-right)
        for row in range(DISTANCE_TO_BORDER, self.amount_rows):
            for col in range(self.amount_columns - DISTANCE_TO_BORDER):
                if all((bitboard >> ((row - i) * self.amount_columns + col + i)) & 1 for i in range(SECTION_LENGTH)):
                    return True

        return False

    def undo_move(self, column, symbol):
        """
        Undoes a move by clearing the bit in the chosen column.
        :param column: The column where the move was played.
        :param symbol: The symbol that was played in the chosen column.
        """
        for row in reversed(range(self.amount_rows)):
            bit_position = row * self.amount_columns + column
            if symbol == SYMBOL_PLAYER_ONE and (self.player1_board >> bit_position) & 1:
                self.player1_board &= ~(1 << bit_position)
                break
            elif symbol == SYMBOL_PLAYER_TWO and (self.player2_board >> bit_position) & 1:
                self.player2_board &= ~(1 << bit_position)
                break

    def get_winning_move(self, symbol, available_moves):
        """
        Returns the first available move that leads to a win for the given symbol.
        :param symbol: The symbol for which to check for a win.
        :param available_moves: The list of available moves.
        :return: The column index of the first available move that leads to a win for the given symbol.
        """
        for move in available_moves:
            self.play_move(move, symbol)
            if self.check_winner(symbol):
                self.undo_move(move, symbol)
                return move
            self.undo_move(move, symbol)
        return None