class GameBoard():
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
        print("----------")
        for row in self.board:
            print("┃".join(row))
            print("━━━━━━━━━")


    def is_full(self):
        """
        Iterates over the board and checks if every space is occupied.
        If one of the spaces is still empty, the board is not full and False is returned.
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
        If the space in the first row of the given column is empty, True is returned.
        Else the column is full and False is returned.
        """
        if column < self.amount_columns and column >= 0:
            if self.board[0][column] == " ":
                return True

        return False


    def play_move(self, column, symbol):
        """
        Handles the placement of a player's symbol in the chosen column for a move
        in the game. It checks from the bottom of the board upwards for an empty spot
        in the column and places the symbol there if found.
        """
        for row in self.board[::-1]:  # Iterates over the rows of the board from top to bottom
            if(row[column]==" "):
                row[column]=symbol
                break

    #Source: https://github.com/KeithGalli/Connect4-Python/blob/master/connect4.py
    def winning_move(board, piece):
        """
        Iterates over the board to check for a winning move.
        """
        # Check horizontal locations for win
        for c in range(board.amount_columns - 3):
            for r in range(board.amount_rows):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(board.amount_columns):
            for r in range(board.amount_rows - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(board.amount_columns - 3):
            for r in range(board.amount_rows - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(board.amount_columns - 3):
            for r in range(3, board.amount_rows):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True
