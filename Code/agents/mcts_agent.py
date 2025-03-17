import random
import math

from Code.agents.player import Player
from Code.constants import EMPTY
from Code.game_board import GameBoard
import random
import math
from Code.constants import EMPTY

class MCTSAgent(Player):
    def __init__(self, symbol, opponent_symbol, iterations=5000, exploration_constant=1.4):
        super().__init__(symbol, opponent_symbol)
        self.iterations = iterations
        self.exploration_constant = exploration_constant

    def choose_move(self, board):
        root = Node(board, None, None, self.symbol, self.opponent_symbol)
        for _ in range(self.iterations):
            node = self.select(root)
            result = self.simulate(node)
            self.backpropagate(node, result)
        return self.best_child(root).move

    def select(self, node):
        while not node.is_terminal():
            if not node.is_fully_expanded:
                return self.expand(node)
            else:
                node = self.best_child(node)
        return node

    def expand(self, node):
        available_moves = node.board.get_available_moves()
        for move in available_moves:
            if move not in node.children:
                # Spielzug durchführen
                node.board.play_move(move, node.current_player)
                # Neuen Knoten erstellen
                new_node = Node(node.board, node, move, self.opponent_symbol if node.current_player == self.symbol else self.symbol, self.opponent_symbol)
                node.children[move] = new_node
                # Spielzug rückgängig machen
                node.board.undo_move(move, node.current_player)
                if len(available_moves) == len(node.children):
                    node.is_fully_expanded = True
                return new_node
        return node

    def simulate(self, node):
        board = node.board
        current_player = node.current_player
        while not board.is_full():
            available_moves = board.get_available_moves()
            move = random.choice(available_moves)
            board.play_move(move, current_player)
            if board.check_winner(current_player):
                # Spielzug rückgängig machen, bevor das Ergebnis zurückgegeben wird
                board.undo_move(move, current_player)
                return current_player
            current_player = self.opponent_symbol if current_player == self.symbol else self.symbol
        return None

    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            if result == node.current_player:
                node.wins += 1
            node = node.parent

    def best_child(self, node):
        best_score = -float('inf')
        best_child = None
        for child in node.children.values():
            exploit = child.wins / child.visits
            explore = math.sqrt(math.log(node.visits) / child.visits)
            score = exploit + self.exploration_constant * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child


class Node:
    def __init__(self, board, parent, move, current_player, opponent_symbol):
        self.board = board  # Originales Brettobjekt
        self.parent = parent
        self.move = move
        self.current_player = current_player
        self.opponent_symbol = opponent_symbol
        self.children = {}
        self.wins = 0
        self.visits = 0
        self.is_fully_expanded = False  # Attribut, keine Methode

    def is_terminal(self):
        return self.board.is_full() or self.board.check_winner(self.current_player) or self.board.check_winner(self.opponent_symbol)