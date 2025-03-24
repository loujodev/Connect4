from Code.agents.human_player import HumanPlayer
from Code.agents.minimax_agent import MiniMaxAgent
from Code.agents.nn_player import NeuralNetworkPlayer
from Code.agents.random_agent import RandomAgent
from Code.agents.smart_agent import SmartAgent
from Code.bitboard import bitboard
from Code.bitboard.bitboard import BitBoard
from Code.bitboard.bitboard_minimax import BitboardMiniMaxAgent
from Code.machinelearning.model import load_saved_model
from Code.machinelearning.get_game_data import save_data, record_games
from Code.evaluation.evaluation import run_evaluation
from Code.game_logic.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO, AMOUNT_COLUMNS, AMOUNT_ROWS, \
    DISTANCE_TO_BORDER, SECTION_LENGTH
from Code.game_logic.game import play_console_game
from Code.game_logic.game_board import GameBoard



#model = load_saved_model('machinelearning/models/test_model.keras')



player1 = MiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = SmartAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)



#run_evaluation(player1, player2, 10)



X,y = record_games(1000, player1, player2)
save_data(X, y, filename='machinelearning/datasets/minimax_depth4_smartagent_1000games.npz')