#Dimensions to instantiate the Board for Connect4
from pandas.core.interchange.dataframe_protocol import Column

AMOUNT_COLUMNS = 6
AMOUNT_ROWS = 7

#Spaces on the board
EMPTY = " "
SYMBOL_PLAYER_ONE = "X"
SYMBOL_PLAYER_TWO = "O"


###Heuristics for the Minimax Agent to evaluate a given board state

#Moves that create a row for the player
SCORE_WIN = 10000
SCORE_THREE = 5
SCORE_TWO = 2
SCORE_CENTRAL = 1

# Blocking opponent's winning moves
SCORE_BLOCK_OPPONENT_WIN = 1000
SCORE_BLOCK_OPPONENT_THREE = 10

#Length of the section viewed when searching for a row of identical symbols
SECTION_LENGTH = 4

#Distance to the edge of the board to avoid iterating out of bounds when looking at sections of 4
DISTANCE_TO_BORDER = SECTION_LENGTH - 1


#The central columns and rows of the board - depending on the dimensions of the board these can either be one or two
if AMOUNT_COLUMNS % 2 == 0:
    CENTRAL_COLS = [int(AMOUNT_COLUMNS/2)]
else:
    CENTRAL_COLS = [int((AMOUNT_COLUMNS/2) - 0.5), int((AMOUNT_COLUMNS/2) + 0.5)]

if AMOUNT_ROWS % 2 == 0:
    CENTRAL_ROWS = [int(AMOUNT_ROWS/2)]
else:
    CENTRAL_ROWS = [int((AMOUNT_ROWS/2) - 0.5), int((AMOUNT_ROWS/2) + 0.5)]


