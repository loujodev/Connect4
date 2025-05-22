# Connect4 AI Agents 

This Connect4 implementation allows users to play against different AI agents or watch AI agents compete against each other. 
The primary focus is on developing and comparing various AI techniques, including a classic Minimax algorithm and a Machine Learning-based agent using a CNN built with Tensorflow. 
The project also provides a suite of evaluation tools to analyze agent performance based on metrics like win rate, game length, resource utilization, and search efficiency for Minimax.

## Table of Contents
* [Features](#features)
* [Project Structure](#project-structure)
* [Setup and Installation](#setup-and-installation)
* [How to Run](#how-to-run)
* [Configuration via `constants.py`](#configuration-via-constantspy)
* [Running Evaluations](#running-evaluations)
* [ML Agent Details](#ml-agent-details)

## Features

* Playable Connect4 game logic.
* Multiple AI agents:
    * Random Agent
    * Smart Agent 
    * Minimax Agent 
    * ML-trained Agent
* Human player option for interactive gameplay.
* Configurable game parameters:
    * Board dimensions (rows, columns).
    * Winning condition (number of pieces in a row).
    * Minimax search depth and evaluation heuristics.
    * Important: ML Agent was trained on a 6x7 board grid and a winninig condition of 4 in a row.
* Agent evaluation framework:
    * Accuracy metrics (win/loss/draw rates).
    * Minimax performance analysis (nodes expanded, branching factor).
    * Resource utilization metrics (memory usage, execution time per move).
* Unit tests for core game logic.

## Setup and Installation

To use this code on your own, set up a Python 3.9 environment and run the following command to install all required packages.
```
pip install -r Connect4/Code/requirements.txt 
```

## How to Run

Direct to the `main.py` file in `Code/main.py`
When creating instances of player agents (classes inheriting from `Player`), it is crucial to correctly assign their `symbol` and `opponent_symbol` parameters during initialization.
Each agent needs to know which game piece it represents and which piece its opponent uses.

The standard symbols are defined in `Code/environment/constants.py` as `SYMBOL_PLAYER_ONE` ("●") and `SYMBOL_PLAYER_TWO` ("○").

**Important:** For a game to function correctly, the two competing agents must have complementary symbol assignments.

**Correct Example:**


```
player1 = MiniMaxAgent(symbol=SYMBOL_PLAYER_ONE, opponent_symbol=SYMBOL_PLAYER_TWO)

player2 = SmartAgent(symbol=SYMBOL_PLAYER_TWO, opponent_symbol=SYMBOL_PLAYER_ONE)

play_console_game(player1, player2)
```

Now player1 and player2 can play against each other correctly.

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


## Running Evaluations

The `Code/evaluation/evaluation.py` script contains functions to assess agent performance:

* `eval_accuracy_metric`: Simulates games and plots win/loss/draw statistics.
* `evaluate_game_level_metrics`: Analyzes game length and winning patterns.
* `evaluate_minimax`: Specifically for TrackedMiniMaxAgent, analyzes nodes expanded, branching factor, and cutoffs.
* `evaluate_memory_usage`: Estimates peak memory allocation during choose_move.
* `evaluate_move_time`: Measures and plots execution time of choose_move.

To run these, modify `Code/main.py` to call the desired evaluation function with the configured agents

The results of these will automatically be saved to `Code/evaluation/Plots` and will be named after the agents that played against each othetr.

### Example:
![TrackedMiniMaxAgent_vs_SmartAgent_nodes_per_move_hist](https://github.com/user-attachments/assets/487b27f7-f1b1-443f-b518-4ced5c787376)

![MlAgent_vs_MiniMaxAgent](https://github.com/user-attachments/assets/337eb9c1-830c-4344-af36-b1b25c5db10d)

## ML Agent Details

* Model Architecture: The MLAgent uses a Convolutional Neural Network (CNN). The architecture (layers like `Conv2D`, `Dense`, `Dropout`) is defined in `Code/agents/MLAgent/model.py`.
* Data Generation: Game data for training the ML model can be generated using functions in `Code/agents/MLAgent/get_game_data.py`. This typically involves simulating games between other agents (e.g., Minimax) and recording board states and moves.
* Training: The notebook `Code/agents/MLAgent/datasets/train_model.py.ipynb` outlines the process for training the CNN model using the generated game data. It includes steps for loading data, building the model, setting up callbacks, and fitting the model. The actual model provided (final_model.keras) was trained using exactly this process.

The training data contained about 350.000 board states as input variable and the chosen move by the Minimax-Agent as output variables in the given situation.

![model_loss](https://github.com/user-attachments/assets/09056dc1-d451-4f59-8150-4710c8dec4b9)




