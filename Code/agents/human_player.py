from Code.agents.player import Player


class HumanPlayer(Player):
    """
    The HumanPlayer class represents a human player.
    It inherits from the Player class.
    It enables playing against an agent or another human player, choosing the moves by entering them into the terminal.


    """
    def choose_move(self, board):
        """
        Lets the player choose a column and loops the input until a valid move is chosen.
        """
        while True:
            try:
                chosen_move = int(input("Player 1, choose a column: "))

                if board.valid_move(chosen_move):
                    return chosen_move
                else:
                    print("Invalid move")
                    print(f"Please choose a number between 0 and {board.amount_columns - 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")