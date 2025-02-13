from numpy.ma.core import bitwise_or

from Code import random_agent
from Code.game_board import GameBoard
from Code.random_agent import RandomAgent


class Game:
    def play_game(self):
        print("Welcome to Connect 4")
        print("")
        board = GameBoard(amount_columns=6, amount_rows=7)
        random_ai = RandomAgent()

        # Game continues while the board is not full and there is no winner
        while not board.is_full():
            board.print_board()
            input_player1 = int(input("Choose a column: "))

            # Repeatedly asks the user to enter a number until there is entered a valid move
            while not board.valid_move(input_player1):
                print("Invalid move")
                print(f"Please choose a number between 0 and {board.amount_columns - 1}")
                input_player1 = int(input("Choose a column: "))

            board.play_move(input_player1, "X")
            board.print_board()

            if board.get_winner():
                print("Player 1 wins!")
            if board.is_full():
                break

            # Random agent's move
            board.play_move(random_ai.random_move(board), "O")
            board.print_board()


game = Game()
game.play_game()