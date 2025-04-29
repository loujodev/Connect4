from Code.agents.MiniMaxAgent.minimax_agent import MiniMaxAgent
from Code.agents.MiniMaxAgent.tracked_minimax_agent import TrackedMiniMaxAgent

from Code.agents.smart_agent import SmartAgent
#from Code.agents.nn_player import NeuralNetworkPlayer
from Code.environment.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO
from Code.evaluation.evaluation import run_evaluation, evaluate_minimax

player1 = TrackedMiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = SmartAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)
#play_console_game(player1, player2)



evaluate_minimax(player1, player2, num_games=100)
