
from Code.agents.minimax_agent import MiniMaxAgent
#from Code.agents.nn_player import NeuralNetworkPlayer
from deprecated.bitboard.bitboard_minimax import BitboardMiniMaxAgent
from Code.game_logic.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO
from Code.game_logic.game import play_console_game
#from Code.game_logic.game_board import GameBoard
#from Code.machinelearning.get_game_data import load_data
#from Code.machinelearning.model import create_connect4_model, train_model
#model = load_saved_model('machinelearning/models/test_model.keras')



player1 = BitboardMiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = MiniMaxAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)



play_console_game(player1, player2)

#run_evaluation(player1, player2, 10)


#X,y = record_games(1000, player1, player2)
#save_data(X, y, filename='machinelearning/datasets/minimax_depth4_smartagent_1000games.npz')