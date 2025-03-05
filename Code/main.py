from Code.Agents.human_player import HumanPlayer
from Code.Agents.minimax_agent import MiniMaxAgent
from Code.Agents.random_agent import RandomAgent
from Code.Agents.smart_agent import SmartAgent
from Code.Evaluation.run_eval import run_evaluation
from Code.constants import SYMBOL_PLAYER_ONE,SYMBOL_PLAYER_TWO
from Code.game import play_console_game

player1 = MiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = SmartAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)


#play_console_game(player1, player2)

run_evaluation(player1, player2, 10)

