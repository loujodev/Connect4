To use this code on your own, set up a Python 3.9 environment and run
"pip install -r Connect4/Code/requirements.txt" to install all required packages.

Inside the main.py file you can then initialize two agents and let them play against each other by either using
the 'play_console_game' function in 'Code/environment/game.py' or using any of the evaluation functions inside 'Code/evaluation/evaluation.py'.

## Agent Initialization

When creating instances of player agents (classes inheriting from `Player`), it is crucial to correctly assign their `symbol` and `opponent_symbol` parameters during initialization.
Each agent needs to know which game piece it represents and which piece its opponent uses.

The standard symbols are defined in `Code/environment/constants.py` as `SYMBOL_PLAYER_ONE` ("●") and `SYMBOL_PLAYER_TWO` ("○").

**Important:** For a game to function correctly, the two competing agents must have complementary symbol assignments.

**Correct Example:**


# Player 1 uses SYMBOL_PLAYER_ONE, knows opponent uses SYMBOL_PLAYER_TWO
player1 = MiniMaxAgent(symbol=SYMBOL_PLAYER_ONE, opponent_symbol=SYMBOL_PLAYER_TWO)

# Player 2 uses SYMBOL_PLAYER_TWO, knows opponent uses SYMBOL_PLAYER_ONE
player2 = SmartAgent(symbol=SYMBOL_PLAYER_TWO, opponent_symbol=SYMBOL_PLAYER_ONE)

# Now player1 and player2 can play against each other correctly.




**MlAgent**

The constructor of the MlAgent takes a third parameter (model_path).
To use the MlAgent inside 'Code/main.py' add the parameter "model_path="agents/MLAgent/final_model.keras" inside the constructor.

**Correct Example:**

player1 = MlAgent(SYMBOL_PLAYER_ONE , SYMBOL_PLAYER_TWO, model_path="agents/MLAgent/final_model.keras")

The Agent was trained with about 350.000 board states and the moves that the MiniMaxAgent chose on the given board state.

He was trained on Google Colab - notebook:




## Configuration via `constants.py`

Several key game parameters and agent behaviors can be adjusted by modifying
the values in the `Code/environment/constants.py` file. This allows customization of the game rules and agent performance.

Key configurable parameters include:

* **Board Dimensions:**
    * `AMOUNT_COLUMNS`: Sets the number of columns on the game board. (must be positive)
    * `AMOUNT_ROWS`: Sets the number of rows on the game board. (must be positive)
* **Winning Condition:**
    * `SECTION_LENGTH`: Defines the number of consecutive pieces required in a line (horizontally, vertically, or diagonally) to win the game. Changing this modifies the fundamental goal (e.g., Connect 4 vs. Connect 5).
* **Minimax Agent Parameters:**
    * `SEARCH_DEPTH`: Controls how many moves ahead the Minimax agent looks. Higher values increase difficulty and computation time.
    * **Evaluation Scores:** These constants define the heuristics used by the Minimax agent to evaluate board positions:
        * `SCORE_WIN`, `SCORE_THREE`, `SCORE_TWO`: Values assigned for achieving or nearing a winning line for the agent.
        * `SCORE_CENTRAL`: Bonus for controlling central columns.
        * `SCORE_BLOCK_OPPONENT_WIN`, `SCORE_BLOCK_OPPONENT_THREE`: Values assigned (negatively) for preventing the opponent from achieving winning or near-winning lines. Modifying these scores will change the Minimax agent's strategy and priorities.


As discussed in a conversation about enhancements in the course, it is also possible to play the game as Connect5/6 or on other board dimensions.
Every of the agents is able to play with any of the adjustable parameters.
Nevertheless, it is not recommended to use the model of the MlAgent on different board dimensions or with a SECTION_LENGTH other than 4
because these where the metrics he was trained on.



**Sources used for the assessment**

*minimax and bitboard
                   Source 1: http://blog.gamesolver.org
                   Source 2: https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
                   Source 3: https://www.youtube.com/watch?v=y7AKtWGOPAE&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV&index=5

*branching factor
                    Source 1: https://www.youtube.com/watch?v=4CxiX2JbY_M
                    Source 2: https://github.com/vivin/cse598/blob/master/mt1/AI_midterm_notes.md #explanation at 'heuristic development'

*Used for the ML Agent  (Started this before enrolling in the university course)
                    Source 1: https://www.coursera.org/learn/machine-learning?specialization=machine-learning-introduction #CNNs and FNNs
                    Source 2: https://www.coursera.org/learn/advanced-learning-algorithms?specialization=machine-learning-introduction #ML basics

*Colorful console outputs
                    Source 1: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
