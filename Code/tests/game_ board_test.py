from Code.game_board import GameBoard
import pytest

def test_is_full():
    full_board =GameBoard(6,7)
    empty_board = GameBoard(6,7)

    assert empty_board.is_full() == False