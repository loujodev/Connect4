from Code.agents.MLAgent.MLAgent import MlAgent
from Code.agents.MiniMaxAgent.minimax_agent import MiniMaxAgent
from Code.agents.MiniMaxAgent.tracked_minimax_agent import TrackedMiniMaxAgent
from Code.agents.random_agent import RandomAgent
from Code.agents.smart_agent import SmartAgent
from Code.environment.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO
from Code.environment.game import play_console_game
from Code.evaluation.evaluation import eval_accuracy_metric, evaluate_minimax, evaluate_game_level_metrics, \
    evaluate_move_time
import warnings
# Suppress the specific UserWarning from urllib3 (should only occur on macOS)
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")


def main():
    player1 = TrackedMiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
    player2 = SmartAgent(SYMBOL_PLAYER_TWO,SYMBOL_PLAYER_ONE)
    evaluate_minimax(player1, player2,500)


if __name__ == "__main__":
    main()



