#Dimensions to instantiate the Board for Connect4
AMOUNT_COLUMNS = 6
AMOUNT_ROWS = 7

#Heuristics for the Minimax Agent to evaluate a given board state
SCORE_WIN = 10000
SCORE_CENTRAL = 4
SCORE_TWO = 2
SCORE_THREE = 5

SCORE_BLOCK_OPPONENT_WIN = 10
SCORE_BLOCK_OPPONENT_THREE = 1

SCORE_OPPONENT_TWO = -2
SCORE_OPPONENT_THREE = -100

#Distance to the edge of the board to avoid iterating out of bounds when viewing sections of 4
DISTANCE_TO_BORDER = 3

#Length of the section viewed when searching for a row of identical symbols
SECTION_LENGTH = 4