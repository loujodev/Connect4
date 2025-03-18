from Code.agents.human_player import HumanPlayer
from Code.agents.minimax_agent import MiniMaxAgent

from Code.evaluation.evaluation import run_evaluation
from Code.game_logic.constants import SYMBOL_PLAYER_ONE, SYMBOL_PLAYER_TWO
from Code.game_logic.game import play_console_game
from Code.game_logic.game_board import GameBoard

player1 = MiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = HumanPlayer(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)


play_console_game(player1, player2)

#run_evaluation(player1, player2, 500)


#board = GameBoard(6,7)
#board.play_move(2, SYMBOL_PLAYER_ONE)
#board.print_board()

#v = flatten_board(board)
#print(v)