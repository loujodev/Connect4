from random import randrange

class RandomAgent():
    def random_move(self, board):
        col = randrange(board.amount_columns)
        while not board.valid_move(col):
            col = randrange(board.amount_columns)
        return col
