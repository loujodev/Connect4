from abc import ABC, abstractmethod
from tkinter.font import names


class Player(ABC):
    def __init__(self,symbol, opponent_symbol):
        self.symbol = symbol
        self.opponent_symbol = opponent_symbol



    @abstractmethod
    def choose_move(self, board):
        pass
