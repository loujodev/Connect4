from Code.agents.minimax_agent import MiniMaxAgent
from Code.agents.nn_player import NeuralNetworkPlayer
from Code.agents.random_minimax_agent import RandomMiniMaxAgent
from Code.agents.smart_agent import SmartAgent
from Code.game_logic.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO, AMOUNT_COLUMNS, AMOUNT_ROWS, \
    DISTANCE_TO_BORDER, SECTION_LENGTH
from Code.game_logic.game import play_console_game
from Code.game_logic.game_board import GameBoard
from Code.machinelearning.model import create_connect4_model

#model = load_saved_model('machinelearning/models/test_model.keras')



player1 = MiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = RandomMiniMaxAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)

model = create_connect4_model()
nn = NeuralNetworkPlayer()


play_console_game(player1, player2)

#run_evaluation(player1, player2, 10)



#X,y = record_games(1000, player1, player2)
#save_data(X, y, filename='machinelearning/datasets/minimax_depth4_smartagent_1000games.npz')