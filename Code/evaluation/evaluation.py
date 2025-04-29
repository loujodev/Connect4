import math
import os
import random

import matplotlib.pyplot as plt
import numpy as np

from Code.agents.MiniMaxAgent.tracked_minimax_agent import TrackedMiniMaxAgent
from Code.environment.constants import SECTION_LENGTH, AMOUNT_COLUMNS, AMOUNT_ROWS, SEARCH_DEPTH
from Code.environment.game import play_game
from tqdm import tqdm

from Code.environment.game_board import GameBoard


def run_evaluation(player1, player2, num_games):
    """
    Runs a given number of games against each other and saves the plot to a file.
    :param player1: Agent 1
    :param player2: Agent 2
    :param num_games: Number of games to run
    :return: None
    """
    draws = 0
    player1_wins = 0
    player2_wins = 0
    player1_first_move =0
    player2_first_move =0

    win_by_making_first_move = 0
    
    #Running the given number of games. Using tqdm to display a progress bar while running the loop
    for _ in tqdm(range(num_games), desc="Simulating Games", unit="game"):
        result, player_making_first_move  = play_game(player1, player2)


        if result == -1:
            draws += 1
        elif result == 0:
            player1_wins += 1
        elif result == 1:
            player2_wins += 1
            
        #If the player who made the first move wins, the counter increments
        if player_making_first_move == result:
            win_by_making_first_move += 1
            
    labels = ["Draws",
              f"{player1.name}",
              f"{player2.name}",
              "Win by playing first move"
              ]

    values = [draws, player1_wins, player2_wins, win_by_making_first_move]

    # Plotting the results
    plt.bar(labels, values, color=["gray", "blue", "red", "green"])
    plt.ylabel("Number of Games")
    plt.title(f"Connect {SECTION_LENGTH} Game Results ")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    print(f"{player1.name} win ratio: {float(player1_wins/num_games)}")
    print(f"{player2.name} win ratio: {float(player2_wins / num_games)}")
    print(f"Draw ratio: {float(draws / num_games)}")
    print(f"Wins by making first move: {float(win_by_making_first_move) / num_games}")

    save_plot(player1, player2, plt)


def save_plot(player1, player2, plot):
    """
    Saves a plot to evaluate of two agents that played various games against each other to "Code/evaluation/Plots".
    :param player1: Agent 1
    :param player2: Agent 2
    :param plot: The plot to save
    :return: None
    """

    output_dir = "evaluation/Plots"

    #Creates a file name by using the class names of the agents that played against each other
    output_file = f"{player1.name}_vs_{player2.name}.png"

    #Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)

    # Save the plot
    output_path = os.path.join(output_dir, output_file)
    plot.savefig(output_path, bbox_inches="tight")
    plot.close()

def evaluate_minimax(minimax_agent: TrackedMiniMaxAgent, opponent, num_games):
    """
    Evaluates the performance of a minimax agent using its tracked version which contains
    :param minimaxagent: An instance of TrackedMiniMaxAgent
    :param oponnent: an instance of player.
    :param num_games: Number of games to run.
    """
    output_dir = "evaluation/Plots"
    all_nodes_expanded_per_move = []
    all_effective_branching_factors = []
    all_search_depths_used = []
    game_avg_nodes = []
    game_avg_branching_factors = []


    # Running the given number of games. Using tqdm to display a progress bar while running the loop
    for _ in tqdm(range(num_games), desc="Simulating Games", unit="game"):
        turn = random.randint(0, 1)
        game_over = False
        board = GameBoard(AMOUNT_COLUMNS, AMOUNT_ROWS)

        while not game_over:
            turn = turn + 1
            turn = turn % 2

            if turn == 1:
                symbol = minimax_agent.symbol
                chosen_move = minimax_agent.choose_move(board)
                metrics = minimax_agent.get_last_move_metrics()
                nodes = metrics['nodes_expanded']
                depth = metrics['search_depth']

                #Source 1: https://www.youtube.com/watch?v=4CxiX2JbY_M
                #Source 2: http://ozark.hendrix.edu/~ferrer/courses/335/f11/lectures/effective-branching.html
                eff_branching_factor = math.pow(max(1, nodes), 1.0 / depth) if depth > 0 else 0
                all_effective_branching_factors.append(eff_branching_factor)
                # Only record metrics if a search actually happened (depth > 0)
                if depth > 0 and nodes > 0:
                    all_nodes_expanded_per_move.append(nodes)
                    all_search_depths_used.append(depth)
            else:
                symbol = opponent.symbol
                chosen_move = opponent.choose_move(board)

            board.play_move(chosen_move, symbol)


            if board.check_winner(symbol) or board.is_full():
                game_over = True


        avg_nodes_this_game = minimax_agent.get_average_nodes_per_move()
        game_avg_nodes.append(avg_nodes_this_game)

    avg_nodes = np.mean(all_nodes_expanded_per_move)
    avg_bf = np.mean(all_effective_branching_factors)
    max_nodes = np.max(all_nodes_expanded_per_move)
    avg_searchdepth = np.mean(all_search_depths_used)

    #Histogram of expanded nodes per move
    plt.figure(figsize=(10, 6))
    plt.hist(all_nodes_expanded_per_move, bins=30, color='skyblue', edgecolor='black')
    plt.axvline(float(avg_nodes), color='red', linestyle='dashed', linewidth=1, label=f'Avg: {avg_nodes:.2f}')
    plt.title(f'Distribution of Nodes Expanded per Move ({minimax_agent.name}, Depth {SEARCH_DEPTH})')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_nodes_hist.png"))

    #Histogram of effective Branching Factor per move
    plt.figure(figsize=(10, 6))
    plt.hist(all_effective_branching_factors, bins=30, color='lightgreen', edgecolor='black')
    plt.axvline(avg_bf, color='red', linestyle='dashed', linewidth=1, label=f'Avg: {avg_bf:.2f}')
    plt.title(f'Distribution of Effective Branching Factor ({minimax_agent.name}, Depth {SEARCH_DEPTH})')
    plt.xlabel('Effective Branching Factor (N^(1/d))')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_branching_factor_hist.png"))
    plt.close()

    #Average nodes per game
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_games + 1), game_avg_nodes, marker='o', linestyle='-', color='purple')
    plt.title(f'Average Nodes Expanded per Move - Per Game ({minimax_agent.name})')
    plt.xlabel('Game Number')
    plt.ylabel('Average Nodes Expanded')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_avg_nodes_per_game.png"))
    plt.close()

def evaluate_game_level_metrics(player1, player2, num_games):
