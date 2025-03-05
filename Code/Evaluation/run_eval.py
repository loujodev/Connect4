import os
import matplotlib.pyplot as plt
from Code.game import play_game
from tqdm import tqdm

def run_evaluation(player1, player2, num_games):
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
              f"{player1.__class__.__qualname__} Wins",
              f"{player2.__class__.__qualname__} Wins"
              ]

    values = [draws, player1_wins, player2_wins]

    # Plotting the results
    plt.bar(labels, values, color=["gray", "blue", "red"])
    plt.ylabel("Number of Games")
    plt.title("Connect 4 Game Results ")

    save_plot(player1, player2, plt)

def save_plot(player1, player2, plt):
    output_dir = "Evaluation"
    output_file = f"{player1.__class__.__qualname__}_vs_{player2.__class__.__qualname__}.png"

    #Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
       os.makedirs(output_dir)

    # Save the plot
    output_path = os.path.join(output_dir, output_file)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()