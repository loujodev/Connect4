from Code.agents.MLAgent.MLAgent import MlAgent
from Code.agents.MiniMaxAgent.minimax_agent import MiniMaxAgent
from Code.agents.MiniMaxAgent.tracked_minimax_agent import TrackedMiniMaxAgent

from Code.agents.smart_agent import SmartAgent
#from Code.agents.nn_player import NeuralNetworkPlayer
from Code.environment.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO
from Code.environment.game import play_console_game
from Code.evaluation.evaluation import eval_accuracy_metric, evaluate_minimax, evaluate_game_level_metrics

player1 = MlAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO, model_path="/agents/MLAgent/final_model.keras")
player2 = MiniMaxAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)
play_console_game(player1, player2)



