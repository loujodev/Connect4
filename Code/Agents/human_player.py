from Code.Agents.player import Player


class HumanPlayer(Player):

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