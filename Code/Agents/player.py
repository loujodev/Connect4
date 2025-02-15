from abc import ABC, abstractmethod

class Player(ABC):
    """
    This abstract class works as a template for all Agent classes.
    Each agent needs to implement the choose_move method and have the properties symbol and opponent_symbol.
    """
    def __init__(self,symbol, opponent_symbol):
        self.symbol = symbol
        self.opponent_symbol = opponent_symbol

    @abstractmethod
    def choose_move(self, board):
        """
        Abstract method that must be implemented by subclasses.
        Should return the column index of the chosen move.
        """
        pass

    def check_winning_move(self, board, symbol, available_moves):
        """
        Returns the first available move that leads to a win for the given symbol by playing the move, checking if
        it leads to a win and then undoing the move.

        param board: The current game board.
              symbol: The symbol for which to check for a win.
              available_moves: The list of available moves.
        :return: The column index of the first available move that leads to a win for the given symbol.
        """
        for move in available_moves:
            board.play_move(move, symbol)
            if board.check_winner(symbol):  #If
                board.undo_move(move,symbol)
                return move
            board.undo_move(move,symbol)  # Undo the move after checking
        return None