import random
from Code.Agents.player import Player



class SmartAgent(Player):

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
        available_moves = board.get_available_moves()

        if not available_moves:
            return None  # No available moves

        #Check for a winning move, if one is found, the agent returns it
        winning_move = board.get_winning_move(self.symbol, available_moves)
        if winning_move is not None:
            print("Smart Agent found a winning move!")
            return winning_move

        #Check for a blocking move, if one is found, the agent returns it
        blocking_move = board.get_winning_move(self.opponent_symbol, available_moves)
        if blocking_move is not None:
            print("Smart Agent found a blocking move!")
            return blocking_move


        #Neither a winning nor a blocking move is found, therefore a random move is returned
        else:
            return available_moves[random.randint(0, len(available_moves)-1)]







