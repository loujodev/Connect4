import os
import matplotlib.pyplot as plt
from Code.constants import SECTION_LENGTH
from Code.game import play_game
from tqdm import tqdm


def save_plot(player1, player2, plot):
    """
    Saves a plot to evaluate of two agents that played various games against each other to "Code/Evaluation/Plots".
    :param player1: Agent 1
    :param player2: Agent 2
    :param plot: The plot to save
    :return: None
    """

    output_dir = "Evaluation/Plots"

    #Creates a file name by using the class names of the agents that played against each other
    output_file = f"{player1.name}_vs_{player2.name}.png"

    #Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)

    # Save the plot
    output_path = os.path.join(output_dir, output_file)
    plot.savefig(output_path, bbox_inches="tight")
    plot.close()

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

    for _ in tqdm(range(num_games), desc="Simulating Games", unit="game"):
        result = play_game(player1, player2)
        if result == 0:
            draws += 1
        elif result == 1:
            player1_wins += 1
        elif result == 2:
            player2_wins += 1

    labels = ["Draws",
              f"{player1.name} Wins",
              f"{player2.name} Wins"
              ]

    values = [draws, player1_wins, player2_wins]

    # Plotting the results
    plt.bar(labels, values, color=["gray", "blue", "red"])
    plt.ylabel("Number of Games")
    plt.title(f"Connect {SECTION_LENGTH} Game Results ")

    print(f"{player1.name} win ratio: {float(player1_wins/num_games)}")
    print(f"{player2.name} win ratio: {float(player2_wins / num_games)}")
    print(f"Draw ratio: {float(draws / num_games)}")

    save_plot(player1, player2, plt)

