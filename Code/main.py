from Code.agents.human_player import HumanPlayer
from Code.agents.minimax_agent import MiniMaxAgent
from Code.agents.mcts_agent import MCTSAgent
from Code.agents.random_agent import RandomAgent
from Code.agents.smart_agent import SmartAgent
from Code.evaluation.evaluation import run_evaluation
from Code.constants import SYMBOL_PLAYER_ONE,SYMBOL_PLAYER_TWO
from Code.game import play_console_game
from Code.game_board import GameBoard

player1 = MiniMaxAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO)
player2 = HumanPlayer(SYMBOL_PLAYER_TWO , SYMBOL_PLAYER_ONE)


play_console_game(player1, player2)

#run_evaluation(player1, player2, 50)



