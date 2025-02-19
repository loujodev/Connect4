#Dimensions to instantiate the Board for Connect4
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


#Moves that block a line of three or four for the opponent
SCORE_BLOCK_OPPONENT_WIN = 10
SCORE_BLOCK_OPPONENT_THREE = 1


SCORE_OPPONENT_CREATE_THREE = -30
SCORE_OPPONENT_CREATE_FOUR = -100

#Distance to the edge of the board to avoid iterating out of bounds when viewing sections of 4
DISTANCE_TO_BORDER = 3

#Length of the section viewed when searching for a row of identical symbols
SECTION_LENGTH = 4

#The central columns of the board - Used by the MiniMax Agent to calculate the score of a move
CENTRAL_COLS = (2,3)
CENTRAL_ROW = (4)