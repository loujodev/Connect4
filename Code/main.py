from Code.Agents.random_agent import RandomAgent
from Code.Agents.smart_agent import SmartAgent
from Code.game import Game

human = RandomAgent("O","X")
smart = SmartAgent("X","O")

game = Game()
game.play_game(smart, human)