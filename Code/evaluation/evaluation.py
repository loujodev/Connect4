import os
import matplotlib.pyplot as plt
from Code.game_logic.constants import SECTION_LENGTH
from Code.game_logic.game import play_game
from tqdm import tqdm

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
              "Wins with playing first move"
              ]

    values = [draws, player1_wins, player2_wins, win_by_making_first_move]

    # Plotting the results
    plt.bar(labels, values, color=["gray", "blue", "red", "green"])
    plt.ylabel("Number of Games")
    plt.title(f"Connect {SECTION_LENGTH} Game Results ")


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