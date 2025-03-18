from Code.game_board import GameBoard
from Code.data.bcolors import  Bcolors
import random
from Code.constants import AMOUNT_ROWS,AMOUNT_COLUMNS


def play_game(player1, player2):
    #Randomize which player gets to start the game
    turn = random.randint(0,1)

    #Saving the player who made the first move in a variable for evaluation
    player_making_first_move = turn

    game_over = False
    board = GameBoard(AMOUNT_COLUMNS, AMOUNT_ROWS)

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

        #Return 0 if it's a draw


        #If the game is won by somebody, return the number of whoever made the winning move
        if board.check_winner(symbol):
            if turn==1:
                return 0, player_making_first_move
            else:
                return 1, player_making_first_move

        #If it's a draw return a 0
        elif board.is_full():
            return -1, player_making_first_move



def play_console_game(player1, player2):

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


