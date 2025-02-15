from random import randrange
from Code.Agents.player import Player


class SmartAgent(Player):
    def __init__(self, symbol, opponent_symbol):
        super().__init__(symbol, opponent_symbol)

    def choose_move(self, board):
        """
        Chooses a move based on the current state of the board

        Step 1: Check for a winning move.
            Step 2: If yes the move is returned.
        Step 3: If not, check for a move to block the opponent’s game.
            Step 4: If yes the move is returned.
        Step 5: In none of the above move exists, the first available move is returned.

        :param board: The current game board.
        :return int: The column index of the chosen move.
        """
        available_moves = self.get_available_moves(board)

        if not available_moves:
            return None  # No available moves

        # Step 1: Check for a winning move
        winning_move = self.check_winning_move(board, self.symbol, available_moves)
        if winning_move:
            print("Winning move found!")
            return winning_move

        # Step 2: Check for a blocking move
        blocking_move = self.check_winning_move(board, self.opponent_symbol, available_moves)
        if blocking_move:
            print("Blocking move found!")
            return blocking_move


        #Choose a random move
        return available_moves[randrange(len(available_moves))]








