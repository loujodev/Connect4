class GameBoard():
    def __init__(self, amount_columns, amount_rows):
        """
        Initializes an empty board with given amount of column and rows.
        Each element in the board is a string with a space as default value.
        """
        self.board = [[ " " for x in range(amount_columns)] for y in range(amount_rows)]

    def print_board(self):
        """
        Iterates over the board and prints each row with a line underneath.
        """
        print("----------")
        for row in self.board:
            print("I".join(row))
            print("----------")


    def check_if_board_full(self):
        """
        Iterates over the board and checks if every space is occupied.
        If one of the spaces is still empty, the board is not full and False is returned.
        If both loops are finished, the board is full and True is returned.
        """
        for row in self.board:
            for element in row:
                if element == " ":
                    return False
        return True

    def check_validity_of_move(self, column):
        """
        Checks if the given column results in a valid move.
        If the space in the first row of the given column is empty, True is returned.
        Else the column is full and False is returned.
        """
        if(self.board[0][column] == " "):
            return True
        else:
            return False


    def play_move(self, column, symbol):
        """
        Handles the placement of a player's symbol in the chosen column for a move
        in the game. It checks from the bottom of the board upwards for an empty spot
        in the column and places the symbol there if found.

        :param column: The index of the column where the symbol should be placed.
                       This must be a valid column within the board.
        :type column: int
        :param symbol: The symbol representing the player's move (e.g., "X" or "O").
        :type symbol: str
        :return: None; modifies the board in place.
        """
        for row in self.board[::-1]:  # Iterates over the rows of the board from top to bottom
            if(row[column]==" "):
                row[column]=symbol
                break