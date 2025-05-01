from Code.environment.game_board import GameBoard
from Code.environment.bcolors import  Bcolors
import random
from Code.environment.constants import AMOUNT_ROWS,AMOUNT_COLUMNS


def initialize_game():
    """
    Creates an efmpty game board, randomizes which player makes the first move and initializes a false/
    boolean to indicate that the game is not over yet

    :return turn: can either be zero or one and determines which player makes the first move
            game_over: False to indicate that the game is not over
            board: Empty game board

    """
    turn = random.randint(0, 1)
    game_over = False
    board = GameBoard(AMOUNT_COLUMNS, AMOUNT_ROWS)

    return turn, game_over, board


def turn_based_move (player1, player2, board, turn):
    """
    Increments the turn variable and places the symbol of the player who's current turn it is on the board
    :param player1: An instance of Player class
    :param player2: An instance of Player class
    :param board: Current board state
    :param turn: Indicates which player has to make a move
    :return: symbol of the current player and the move he made
    """
    turn = turn + 1
    turn = turn % 2

    if turn == 1:
        symbol = player1.symbol
        chosen_move = player1.choose_move(board)
    else:
        symbol = player2.symbol
        chosen_move = player2.choose_move(board)

    board.play_move(chosen_move, symbol)
    return chosen_move, symbol, turn


def play_game(player1, player2):
    """
    Plays the game between two players without printing the current board state after each move.
    :param player1: Instance of Player class
    :param player2: Instance of Player class
    :return: An integer indicating which player won (1 = player1, 0 = player2, -1=draw)
             An integer indicating which player made the first move to analyze if it had an impact on the outcome of the game.
    """
    turn, game_over, board = initialize_game()

    # Saving the player who made the first move in a variable for evaluation
    player_making_first_move = turn

    # Game continues while the board is not full and there is no winner
    while not game_over:
        chosen_move, symbol, turn = turn_based_move(player1, player2, board, turn)

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
    """
    Enables playing a game and printing the current board state after each move.
    :param player1: An instance of Player class
    :param player2: An instance of Player class
    :return: None
    """
    turn, game_over, board = initialize_game()

    print(f"{Bcolors.BOLD} Welcome to Connect 4")
    print("")
    board.print_board()

    # Game continues while the board is not full and there is no winner
    while not game_over:

        chosen_move, symbol, turn = turn_based_move(player1, player2, board, turn)

        if board.is_full():
            print(f"{Bcolors.YELLOW}It's a tie!")
            game_over = True
        elif board.check_winner(symbol):
            print(f"{Bcolors.GREEN}Player {symbol} wins!")
            game_over = True

        board.print_board()


