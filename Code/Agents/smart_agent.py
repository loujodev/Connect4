import copy

from Code.Agents.player import Player


class SmartAgent(Player):
    def __init__(self, symbol, opponent_symbol):
        super().__init__(symbol, opponent_symbol)


    def get_available_moves(self, board):
        """
        Returns a list of all available moves on the board
        """
        available_moves = []
        for col in range(board.amount_columns):
            if board.valid_move(col):
                available_moves.append(col)
        return available_moves

    def check_winning_move(self, board, symbol, available_moves):
        """
        Returns the first available move that leads to a win for the given symbol
        """
        for move in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy.play_move(move,symbol)

            if board_copy.check_winner(symbol):
                return move

    def choose_move(self, board):
        """
        Chooses a move based on the current state of the board

        Step 1: Checks if there is a winning move
        Step 2: Checks if there is a move that blocks the opponent from winning
        Step 3: Checks if there is a move that would lead to a winning move for the opponent
                and remove it from the available moves
        Step 4: Choose a random move
        """
        available_moves = self.get_available_moves(board)

        #Check for a winning move
        winning_move = self.check_winning_move(board, self.symbol, available_moves)
        if winning_move:
            return winning_move

        #Check for a blocking move
        blocking_move = self.check_winning_move(board, self.opponent_symbol, available_moves)
        if blocking_move:
            return blocking_move

        #Check if a move would lead to a winning move for the opponent
        #Not implemented yet


        #Choose a random move
        return available_moves[0]








