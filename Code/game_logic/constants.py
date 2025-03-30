#Spaces on the board
EMPTY = " "
SYMBOL_PLAYER_ONE = "●"
SYMBOL_PLAYER_TWO = "○"

#Dimensions to instantiate the Board for Connect4
AMOUNT_COLUMNS = 7
AMOUNT_ROWS = 6

#Number of symbols in a row that are required to Win a game
SECTION_LENGTH = 4

#The central columns of the board - depending on the dimensions of the board these can either be one or two
if AMOUNT_COLUMNS % 2 == 0:
    CENTRAL_COLS = [int(AMOUNT_COLUMNS/2)]
else:
    CENTRAL_COLS = [int((AMOUNT_COLUMNS/2) - 0.5), int((AMOUNT_COLUMNS/2) + 0.5)]


#Distance to the edge of the board to avoid iterating out of bounds when looking at sections of 4
DISTANCE_TO_BORDER = SECTION_LENGTH - 1


###Heuristics for the Minimax Agent to evaluate a given board state

#Moves that create a row for the player
SCORE_WIN = 1000000
SCORE_THREE = 50
SCORE_TWO = 2
SCORE_CENTRAL = 1

#A board state where a player has two moves that lead to a win
SCORE_FORK = 1000

# Blocking opponent's winning moves
SCORE_BLOCK_OPPONENT_WIN = 1000
SCORE_BLOCK_OPPONENT_THREE = 10

#Search Depth of the MiniMaxAgent
SEARCH_DEPTH = 4
BITBOARD_SEARCH_DEPTH = 4







