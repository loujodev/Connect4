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

