from Code.game_board import GameBoard
from Code.bcolors import  bcolors

class Game:
    AMOUNT_COLUMNS = 6
    AMOUNT_ROWS = 7

    def play_game(self, player1, player2):

        turn = 0
        game_over = False
        board = GameBoard(self.AMOUNT_COLUMNS, self.AMOUNT_ROWS)

        print("Welcome to Connect 4")
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
                print(f"{bcolors.YELLOW}It's a tie!")
                game_over = True
            elif board.check_winner(symbol):
                print(f"{bcolors.GREEN}Player {symbol} wins!")
                game_over = True

            board.print_board()

