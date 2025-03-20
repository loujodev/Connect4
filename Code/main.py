from Code.agents.human_player import HumanPlayer
from Code.agents.mcts_agent import MCTSAgent
from Code.agents.minimax_agent import MiniMaxAgent
from Code.agents.smart_agent import SmartAgent
from Code.bitboard import bitboard
from Code.bitboard.bitboard import BitBoard
from Code.bitboard.bitboard_minimax import BitboardMiniMaxAgent
from Code.machinelearning.transform_games import save_data

from Code.evaluation.evaluation import run_evaluation
from Code.game_logic.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO, AMOUNT_COLUMNS, AMOUNT_ROWS, \
    DISTANCE_TO_BORDER, SECTION_LENGTH
from Code.game_logic.game import play_console_game, record_games
from Code.game_logic.game_board import GameBoard

player1 = BitboardMiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = MiniMaxAgent(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)



play_console_game(player1, player2)

#run_evaluation(player1, player2, 4)



#X,y = record_games(100, player1, player2)
#save_data(X,y, filename='minimax_depth6_100games.npz' )