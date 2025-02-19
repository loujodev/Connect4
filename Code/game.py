from Code.game_board import GameBoard
from Code.bcolors import  Bcolors
import random
from Code.constants import AMOUNT_ROWS,AMOUNT_COLUMNS

class Game:
    def play_game(self, player1, player2):

        #Randomize which player gets to start the game
        turn = random.randint(0,1)
        game_over = False
        board = GameBoard(AMOUNT_COLUMNS, AMOUNT_ROWS)

        print(f"{Bcolors.BOLD} Welcome to Connect 4")
        print("")
        board.print_board()

        # Game continues while the board is not full and there is no winner
        while not game_over:

            turn = turn + 1
            turn = turn%2

            if turn==1:
                symbol = player1.symbol
                chosen_move = player1.choose_move(board)
            else:
                symbol = player2.symbol
                chosen_move = player2.choose_move(board)


            board.play_move(chosen_move, symbol)

            if board.is_full():
                print(f"{Bcolors.YELLOW}It's a tie!")
                game_over = True
            elif board.check_winner(symbol):
                print(f"{Bcolors.GREEN}Player {symbol} wins!")
                game_over = True

            board.print_board()

