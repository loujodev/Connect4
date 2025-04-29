from Code.agents.MiniMaxAgent.minimax_agent import MiniMaxAgent
from Code.environment.constants import SEARCH_DEPTH


class TrackedMiniMaxAgent(MiniMaxAgent):
    """
    A MiniMaxAgent that tracks search performance metrics like nodes expanded
    and the depth used for each move decision.
    """
    def __init__(self, symbol, opponent_symbol):
        super().__init__(symbol, opponent_symbol)
        #Track the move total
        self.nodes_expanded_last_move = 0
        self.search_depth_last_move = 0

        #Track the game total
        self.total_nodes_expanded_game = 0 # Tracks nodes for the entire game
        self.move_count_game = 0 # Tracks moves made in the current game
        self.total_cutoffs_game = 0  #Tracks cutoffs of the entire game

    def reset_game_metrics(self):
        """Resets metrics tracked over a single game."""
        self.total_nodes_expanded_game = 0
        self.move_count_game = 0

    def choose_move(self, board):
        """
        Chooses a move using minimax and tracks the number of nodes expanded
        and the search depth used for this specific move.
        """
        # Reset metrics for the current move decision
        self.nodes_expanded_last_move = 0
        self.search_depth_last_move = SEARCH_DEPTH
        self.cutoffs_last_move = 0

        available_moves = board.get_available_moves()

        # --- Performance Checks ---
        performance_move = self.performance_checks(board, available_moves)
        if performance_move is not None:
            self.nodes_expanded_last_move = 1 #Just the current node was visited
            self.search_depth_last_move = 0 # Indicate no deep search was done
            self.move_count_game += 1 # Increment move count
            self.cutoffs_last_move += 1 #Could also be 0, not really sure if this counts as cutoff
            return performance_move



        self.nodes_expanded_last_move = 0 # Reset specifically for the minimax call
        best_move, _ = self.minimax(board, SEARCH_DEPTH, True)

        self.total_nodes_expanded_game += self.nodes_expanded_last_move
        self.total_cutoffs_game += self.cutoffs_last_move
        self.move_count_game += 1

        return best_move

    def minimax(self, board, depth, maximizing, alpha=-float('inf'), beta=float('inf')):
        """
        Overrides the minimax method to count each node expansion.
        """

        #increase the counter of the visited nodes everytime this method is called
        self.nodes_expanded_last_move += 1

        if depth == 0 or self.is_terminal(board):
            if self.is_terminal(board):
                if board.check_winner(self.symbol):
                    return None, float('inf')
                elif board.check_winner(self.opponent_symbol):
                    return None, -float('inf')
                else: # Draw
                    return None, 0
            return None, self.evaluate_position(-1, board)

        available_moves = board.get_available_moves()

        best_move = available_moves[0]  # Default move

        if maximizing:
            value = -float("inf")
            for move in available_moves:
                board.play_move(move, self.symbol)
                _, score = self.minimax(board, depth - 1, False, alpha, beta)
                board.undo_move(move, self.symbol)

                if score > value:
                    value = score
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    # increase the cutoff counter
                    self.cutoffs_last_move += 1
                    break


            return best_move, value

        else:  # minimizing
            value = float("inf")
            for move in available_moves:
                board.play_move(move, self.opponent_symbol)
                _, score = self.minimax(board, depth - 1, True, alpha, beta)
                board.undo_move(move, self.opponent_symbol)

                if score < value:
                    value = score
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    #increase the cutoff counter
                    self.cutoffs_last_move += 1
                    break


            return best_move, value

    def get_last_move_metrics(self):
        """Returns the metrics recorded during the last call to choose_move."""
        return {
            'nodes_expanded': self.nodes_expanded_last_move,
            'search_depth': self.search_depth_last_move,
            'cutoffs': self.cutoffs_last_move
        }

    def get_average_nodes_per_move(self):
        """Calculates the average nodes expanded per move over the current game."""
        if self.move_count_game == 0:
            return 0
        return self.total_nodes_expanded_game / self.move_count_game

    def get_average_cutoffs_per_move(self):
        """Calculates the average alpha-beta cutoffs per move over the current game."""
        if self.move_count_game == 0:
            return 0
        return self.total_cutoffs_game / self.move_count_game