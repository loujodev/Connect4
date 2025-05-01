import math
import os
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from Code.agents.MiniMaxAgent.tracked_minimax_agent import TrackedMiniMaxAgent
from Code.environment.constants import SECTION_LENGTH, AMOUNT_COLUMNS, AMOUNT_ROWS, SEARCH_DEPTH, DISTANCE_TO_BORDER
from Code.environment.game import play_game, initialize_game, turn_based_move
from tqdm import tqdm
from Code.environment.game_board import GameBoard



def eval_accuracy_metric(player1, player2, num_games):
    """
    Evaluates the Accuracy Metrics (win, draw, loss, how many times did the player win who made the first move).
    Runs a given number of games against each other and saves the plot to a file.
    :param player1: Agent 1
    :param player2: Agent 2
    :param num_games: Number of games to run
    :return: None
    """
    draws = 0
    player1_wins = 0
    player2_wins = 0

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
    
def evaluate_game_level_metrics(player1, player2, num_games):
    """
    Saves a plot to evaluate Game-Level Metrics (Game Length and Winning Patterns: frequency of horizontal, vertical, diagonal winning)
    This evaluates only the winning patterns of player 1.
    :param player1: The agent to evaluate the winning patterns of
    :param player2: opponent of player 1
    :param num_games: number of games to run
    :return: None
    """
    output_dir = "evaluation/Plots/game_level_metrics"
    pos_diagonally_wins = 0
    neg_diagonally_wins = 0
    horizontal_wins = 0
    vertical_wins = 0

    game_length_list = []

    for _ in tqdm(range(num_games), desc="Simulating Games", unit="game"):
        turn, game_over, board = initialize_game()
        game_length = 0
        while not game_over:
            chosen_move, symbol, turn = turn_based_move(player1, player2, board, turn)
            game_length +=1

            #Only check the winning pattern for player 1
            if symbol == player1.symbol:

                #Check horizontally
                if board.check_winner(symbol):
                    for row in range(AMOUNT_ROWS):
                        for col in range(AMOUNT_COLUMNS- DISTANCE_TO_BORDER):
                            if all(board.board[row][col + i] == symbol for i in range(SECTION_LENGTH)):
                                horizontal_wins += 1

                    # Check vertically
                    for col in range(AMOUNT_COLUMNS):
                        for row in range(AMOUNT_ROWS- DISTANCE_TO_BORDER):
                            if all(board.board[row + i][col] == symbol for i in range(SECTION_LENGTH)):
                                vertical_wins += 1

                    # Check diagonally (top-left to bottom-right)
                    for row in range(AMOUNT_ROWS - DISTANCE_TO_BORDER):
                        for col in range(AMOUNT_COLUMNS - DISTANCE_TO_BORDER):
                            if all(board.board[row + i][col + i] == symbol for i in range(SECTION_LENGTH)):
                                neg_diagonally_wins += 1

                    # Check diagonally (bottom-left to top-right)
                    for row in range(AMOUNT_ROWS- DISTANCE_TO_BORDER):
                        for col in range(DISTANCE_TO_BORDER,AMOUNT_COLUMNS):
                            if all(board.board[row + i][col - i] == symbol for i in range(SECTION_LENGTH)):
                                pos_diagonally_wins += 1

            if board.check_winner(symbol) or board.is_full():
                game_over = True
                game_length_list.append(game_length)


    #Plot the results
    labels = ["Horizontal Wins",
              "Vertical Wins",
              "Negative Diagonally Wins",
              "Positive Diagonally Wins",
              ]

    values = [horizontal_wins, vertical_wins, neg_diagonally_wins, pos_diagonally_wins]

    # Plotting the results for winning patterns
    plt.bar(labels, values, color=["gray", "blue", "red", "green"])
    plt.ylabel("Number of Games")
    plt.title(f"Wining patterns of {player1.name} against {player2.name}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{player1.name}_vs_{player2.name}_winning_patterns.png"))

    #Plotting the results of the game length on a histogram
    avg_game_length = np.mean(game_length_list)
    plt.figure(figsize=(10, 6))
    plt.hist(game_length_list, bins=30, color='lightgreen', edgecolor='black')
    plt.axvline(avg_game_length, color='red', linestyle='dashed', linewidth=1,label=f'Avg Moves: {avg_game_length:.2f}')
    plt.title(f'Distribution of game length ({player1.name} vs {player2.name})')
    plt.xlabel('Game Length (Number of moves)')
    plt.ylabel('Frequency (Number of games)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{player1.name}_vs_{player2.name}_game_length_hist.png"))

def save_plot(player1, player2, plot):
    """
    Saves a plot to evaluate of two agents that played various games against each other to "Code/evaluation/Plots".
    :param player1: Agent 1
    :param player2: Agent 2
    :param plot: The plot to save
    :return: None
    """

    output_dir = "evaluation/Plots/win_loss_rate"

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
    :param minimax_agent: An instance of TrackedMiniMaxAgent
    :param opponent: an instance of player.
    :param num_games: Number of games to run.
    """
    output_dir = "evaluation/Plots/minimax_performance"
    all_nodes_expanded_per_move = []
    all_effective_branching_factors = []
    all_search_depths_used_per_move = []
    all_cutoffs_per_move = []

    game_avg_nodes = []
    game_avg_cutoffs = []



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
                cutoffs = metrics['cutoffs']


                # Only record metrics if a search actually happened (depth > 0)
                if depth > 0 and nodes > 0:
                    all_nodes_expanded_per_move.append(nodes)

                    all_cutoffs_per_move.append(cutoffs)

                    # Source 1: https://www.youtube.com/watch?v=4CxiX2JbY_M
                    # Source 2: https://github.com/vivin/cse598/blob/master/mt1/AI_midterm_notes.md
                    eff_branching_factor = math.pow(max(1, nodes), 1.0 / depth) if depth > 0 else 0
                    all_effective_branching_factors.append(eff_branching_factor)
            else:
                symbol = opponent.symbol
                chosen_move = opponent.choose_move(board)

            board.play_move(chosen_move, symbol)


            if board.check_winner(symbol) or board.is_full():
                game_over = True


        avg_nodes_this_game = minimax_agent.get_average_nodes_per_move()
        game_avg_nodes.append(avg_nodes_this_game)

        avg_cutoffs_this_game = minimax_agent.get_average_cutoffs_per_move()
        game_avg_cutoffs.append(avg_cutoffs_this_game)


    avg_nodes = np.mean(all_nodes_expanded_per_move)
    avg_bf = np.mean(all_effective_branching_factors)
    avg_cutoffs = np.mean(all_cutoffs_per_move)
    # avg_searchdepth = np.mean(all_search_depths_used)

    #Histogram of expanded nodes per move
    plt.figure(figsize=(10, 6))
    plt.hist(all_nodes_expanded_per_move, bins=30, color='skyblue', edgecolor='black')
    plt.axvline(float(avg_nodes), color='red', linestyle='dashed', linewidth=1, label=f'Avg: {avg_nodes:.2f}')
    plt.title(f'Distribution of nodes expanded per move ({minimax_agent.name}, Depth {SEARCH_DEPTH})')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_nodes_hist.png"))

    #Histogram of effective Branching Factor per move
    plt.figure(figsize=(10, 6))
    plt.hist(all_effective_branching_factors, bins=30, color='lightgreen', edgecolor='black')
    plt.axvline(avg_bf, color='red', linestyle='dashed', linewidth=1, label=f'Avg: {avg_bf:.2f}')
    plt.title(f'distribution of effective branching factor ({minimax_agent.name}, Depth {SEARCH_DEPTH})')
    plt.xlabel('Effective Branching Factor (N^(1/d))')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_branching_factor_hist.png"))


    #Average nodes per game
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_games + 1), game_avg_nodes, marker='o', linestyle='-', color='purple')
    plt.title(f'Average Nodes Expanded per Move - Per Game ({minimax_agent.name} at Depth: {SEARCH_DEPTH})')
    plt.xlabel('Game Number')
    plt.ylabel('Average Nodes Expanded')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_avg_nodes_per_game.png"))

    #Average cutoffs per game
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_games + 1), game_avg_cutoffs, marker='x', linestyle='--', color='orange', label='Avg Cutoffs')
    plt.title(f'Average Alpha-Beta Cutoffs per Move - Per Game ({minimax_agent.name} vs {opponent.name})')
    plt.xlabel('Game Number')
    plt.ylabel('Cutoffs')
    plt.grid(True)
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"{minimax_agent.name}_vs_{opponent.name}_avg_cutoffs_pergame.png"))





# Function to format time in milliseconds
def format_time_ms(seconds):
    return f"{seconds * 1000:.2f} ms"


def evaluate_move_time(player1, player2, num_games):
    """
    Evaluates and plots the execution time of the choose_move method for two agents.
    Runs a given number of games, reports the average and max times, and saves histograms.

    :param player1: Agent 1 (Instance of Player)
    :param player2: Agent 2 (Instance of Player)
    :param num_games: Number of games to simulate
    :return: None
    """
    p1_times = []
    p2_times = []

    for game_num in tqdm(range(num_games), desc="Simulating Games for Time", unit="game"):

        turn, game_over, board = initialize_game()
        player_making_first_move = turn
        current_turn_player_index = player_making_first_move

        while not game_over:
            if current_turn_player_index == 0:
                current_player = player1
                symbol = player1.symbol
            else:
                current_player = player2
                symbol = player2.symbol

            start_time = time.perf_counter()
            chosen_move = current_player.choose_move(board)
            end_time = time.perf_counter()

            elapsed_time = end_time - start_time

            if current_turn_player_index == 0:
                p1_times.append(elapsed_time)
            else:
                p2_times.append(elapsed_time)

            if board.valid_move(chosen_move):
                board.play_move(chosen_move, symbol)
            else:
                print(f"Warning: Agent {current_player.name} chose invalid move {chosen_move} in game {game_num+1}.")
                game_over = True # End game on invalid move
                continue

            if board.check_winner(symbol) or board.is_full():
                game_over = True

            current_turn_player_index = 1 - current_turn_player_index

    # --- Analyze and Report Results ---
    avg_time_p1 = np.mean(p1_times) if p1_times else 0
    avg_time_p2 = np.mean(p2_times) if p2_times else 0
    max_time_p1 = np.max(p1_times) if p1_times else 0
    max_time_p2 = np.max(p2_times) if p2_times else 0


    # --- Plotting ---
    output_dir = "evaluation/Plots/time_usage"
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)

    plt.figure(figsize=(12, 6))

    # Plot for Player 1
    plt.subplot(1, 2, 1)

    # Convert times to ms for plotting
    p1_times_ms = [t * 1000 for t in p1_times]
    plt.hist(p1_times_ms, bins=20, color='cyan', alpha=0.7, label='Time per move')
    plt.axvline(avg_time_p1 * 1000, color='red', linestyle='dashed', linewidth=1, label=f'Avg: {format_time_ms(avg_time_p1)}')
    plt.axvline(max_time_p1 * 1000, color='orange', linestyle='dashed', linewidth=1, label=f'Max: {format_time_ms(max_time_p1)}')


    plt.title(f'Move Times ({player1.name})')
    plt.xlabel('Execution Time (ms)')
    plt.ylabel('Frequency')
    plt.legend()

    # Plot for Player 2
    plt.subplot(1, 2, 2)

    # Convert times to ms for plotting
    p2_times_ms = [t * 1000 for t in p2_times]
    plt.hist(p2_times_ms, bins=20, color='magenta', alpha=0.7, label='Time per move')
    plt.axvline(avg_time_p2 * 1000, color='blue', linestyle='dashed', linewidth=1, label=f'Avg: {format_time_ms(avg_time_p2)}')
    plt.axvline(max_time_p2 * 1000, color='purple', linestyle='dashed', linewidth=1, label=f'Max: {format_time_ms(max_time_p2)}')


    plt.title(f'Move Times ({player2.name})')
    plt.xlabel('Execution Time (ms)')
    # plt.ylabel('Frequency') # Optional if y-axis is shared
    plt.legend()

    plt.suptitle('Distribution of choose_move Execution Time')
    plt.tight_layout()
    plot_filename = os.path.join(output_dir, f"{player1.name}_vs_{player2.name}_move_times_hist.png")

    plt.savefig(plot_filename)



