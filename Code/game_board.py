from Code.constants import DISTANCE_TO_BORDER


class GameBoard:
    def __init__(self, amount_columns, amount_rows):
        """
        Initializes an empty board with given amount of column and rows.
        Each element in the board is a string with a space as default value.
        """
        self.amount_columns = amount_columns
        self.amount_rows = amount_rows
        self.board = [[ " " for x in range(amount_columns)] for y in range(amount_rows)]

    def print_board(self):
        """
        Iterates over the board and prints each row with a line underneath.
        """
        print("------------------------------")
        for row in self.board:
            print("  ┃  ".join(row))
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


    def is_full(self):
        """
        Iterates over the board and checks if every space is occupied.

        :return bool: If one of the spaces is still empty, the board is not full and False is returned.
        Else both loops finish, hence the board is full and True is returned.
        """
        for row in self.board:
            for element in row:
                if element == " ":
                    return False
        return True

    def valid_move(self, column):
        """
        Checks if the given column results in a valid move.
        If the column is out of bounds, the column is already full or the input is not a number,False is returned.
        If the space in the first row of the given column is empty,True is returned.
        """
        if isinstance(column, int) and self.amount_columns > column >= 0:
            if self.board[0][column] == " ":
                return True

        return False

    def get_available_moves(self):
        """
        Determine the list of available moves for the current board state. An available
        move is defined as a column index where a move can be legally made according
        to the board's rules.

        :param self: The game board on which to calculate available moves.
        :return: A list of integers representing the columns where moves are valid.
        """
        available_moves = []
        for col in range(self.amount_columns):
            if self.valid_move(col):
                available_moves.append(col)
        return available_moves


    def play_move(self, column, symbol):
        """
        Handles the placement of a player's symbol in the chosen column for a move
        in the game. It checks from the bottom of the board upwards for an empty spot
        in the column and places the symbol there if found.
        """
        for row in self.board[::-1]:  # Iterates over the rows of the board from top to bottom
            if row[column]==" ":
                row[column]=symbol
                break

    def check_winner(self, symbol):
        """
        Iterates over the board and checks if there are 4 consecutive symbols in any direction.
        :param symbol: The symbol to check for.
        :return bool: True if a winner is found, False otherwise.
        """
        # Check horizontally
        for row in range(self.amount_rows):
            for col in range(self.amount_columns - DISTANCE_TO_BORDER):
                if all(self.board[row][col + i] == symbol for i in range(4)):
                    return True

        # Check vertically
        for col in range(self.amount_columns):
            for row in range(self.amount_rows - DISTANCE_TO_BORDER):
                if all(self.board[row + i][col] == symbol for i in range(4)):
                    return True

        # Check diagonally (top-left to bottom-right)
        for row in range(self.amount_rows - DISTANCE_TO_BORDER):
            for col in range(self.amount_columns - DISTANCE_TO_BORDER):
                if all(self.board[row + i][col + i] == symbol for i in range(4)):
                    return True

        # Check diagonally (bottom-left to top-right)
        for row in range(self.amount_rows - DISTANCE_TO_BORDER):
            for col in range(3, self.amount_columns):
                if all(self.board[row + i][col - i] == symbol for i in range(4)):
                    return True

        return False

    def undo_move(self, column, symbol):
        """
        Undoes a move by replacing the symbol in the chosen column with a space.
        :param column: The column where the move was played.
        """
        for row in self.board:
            if row[column] == symbol:
                row[column] = " "
                break


    def get_winning_move(self, symbol, available_moves):
        """
        Returns the first available move that leads to a win for the given symbol by playing the move, checking if
        it leads to a win and then undoing the move.

        param board: The current game board.
              symbol: The symbol for which to check for a win.
              available_moves: The list of available moves.
        :return: The column index of the first available move that leads to a win for the given symbol.
        """
        for move in available_moves:
            self.play_move(move, symbol)
            if self.check_winner(symbol):  #If
                self.undo_move(move,symbol)
                return move
            self.undo_move(move,symbol)  # Undo the move after checking
        return None

