from Code.game_board import GameBoard
from Code.bcolors import  bcolors

class Game:
    AMOUNT_COLUMNS = 6
    AMOUNT_ROWS = 7

    def play_game(self, player1, player2):
        print("Welcome to Connect 4")
        print("")

        turn = 0
        game_over = False
        board = GameBoard(self.AMOUNT_COLUMNS, self.AMOUNT_ROWS)

        # Game continues while the board is not full and there is no winner
        while not game_over:
            board.print_board()
            turn = turn + 1
            turn = turn%2

            if turn==1:
                chosen_move = player1.choose_move(board)
            else:
                chosen_move = player2.choose_move(board)

            symbol = player1.symbol if turn == 0 else player2.symbol
            board.play_move(chosen_move, symbol)

            if board.is_full():
                print(f"{bcolors.YELLOW}It's a tie!")
                game_over = True
            elif board.check_winner(symbol):
                print(f"{bcolors.GREEN}Player {symbol} wins!")
                game_over = True



