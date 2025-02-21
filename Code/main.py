from Code.Agents.human_player import HumanPlayer
from Code.Agents.minimax_agent import MiniMaxAgent
from Code.Agents.random_agent import RandomAgent
from Code.Agents.smart_agent import SmartAgent
from Code.constants import SYMBOL_PLAYER_ONE,SYMBOL_PLAYER_TWO
from Code.game import Game

player1 = MiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = SmartAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)

game = Game()
game.play_game(player1, player2)