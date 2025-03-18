import pytest
from Code.game_logic.game_board import GameBoard

@pytest.fixture
def game_board():
    return GameBoard(7, 6)

def test_initialization(game_board):
    assert game_board.amount_columns == 7
    assert game_board.amount_rows == 6
    assert all(cell == " " for row in game_board.board for cell in row)


def test_is_full(game_board):
    assert not game_board.is_full()
    for row in range(game_board.amount_rows):
        for col in range(game_board.amount_columns):
            game_board.play_move(col, "X")
    assert game_board.is_full()

def test_valid_move(game_board):
    assert game_board.valid_move(0) == True
    assert game_board.valid_move(6) == True
    assert game_board.valid_move(7) == False
    assert game_board.valid_move(-1) == False
    game_board.play_move(0, "X")
    assert game_board.valid_move(0) == True
    for row in range(game_board.amount_rows):
        game_board.play_move(0, "X")
    assert game_board.valid_move(0) == False

def test_get_available_moves(game_board):
    assert game_board.get_available_moves(game_board) == [0, 1, 2, 3, 4, 5, 6]
    game_board.play_move(0, "X")
    assert game_board.get_available_moves(game_board) == [0, 1, 2, 3, 4, 5, 6]
    for row in range(game_board.amount_rows):
        game_board.play_move(0, "X")
    assert game_board.get_available_moves(game_board) == [1, 2, 3, 4, 5, 6]

def test_play_move(game_board):
    game_board.play_move(0, "X")
    assert game_board.board[5][0] == "X"
    game_board.play_move(0, "O")
    assert game_board.board[4][0] == "O"
    for row in range(game_board.amount_rows):
        game_board.play_move(1, "X")
    assert game_board.board[0][1] == "X"

def test_check_winner_horizontal(game_board):
    for col in range(4):
        game_board.play_move(col, "X")
    assert game_board.check_winner("X") == True

def test_check_winner_vertical(game_board):
    for row in range(4):
        game_board.play_move(0, "X")
    assert game_board.check_winner("X") == True

def test_check_winner_diagonal_top_left_to_bottom_right(game_board):
    for i in range(4):
        game_board.play_move(i, "X")
        for _ in range(i):
            game_board.play_move(i, "O")
    assert game_board.check_winner("X") == True

def test_check_winner_diagonal_bottom_left_to_top_right(game_board):
    for i in range(4):
        game_board.play_move(3 - i, "X")
        for _ in range(i):
            game_board.play_move(3 - i, "O")
    assert game_board.check_winner("X") == True

def test_undo_move(game_board):
    game_board.play_move(0, "X")
    game_board.undo_move(0, "X")
    assert game_board.board[5][0] == " "
    game_board.play_move(0, "X")
    game_board.play_move(0, "O")
    game_board.undo_move(0, "O")
    assert game_board.board[4][0] == " "

def test_check_winner_no_winner(game_board):
    assert game_board.check_winner("X") == False
    assert game_board.check_winner("O") == False

def test_check_winner_full_board_no_winner(game_board):
    for row in range(game_board.amount_rows):
        for col in range(game_board.amount_columns):
            symbol = "X" if (row + col) % 2 == 0 else "O"
            game_board.play_move(col, symbol)
    assert game_board.check_winner("X") == False
    assert game_board.check_winner("O") == False