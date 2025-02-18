from Code.Agents.human_player import HumanPlayer
from Code.Agents.smart_agent import SmartAgent
from Code.game import Game

smart = SmartAgent("X","O")
human = HumanPlayer("O","X")
game = Game()
game.play_game(smart, human)