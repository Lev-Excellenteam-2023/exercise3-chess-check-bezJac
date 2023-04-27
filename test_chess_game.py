import pytest
from unittest.mock import MagicMock
from chess_engine import game_state
import Piece
from enums import Player


@pytest.fixture
def mock_game_state_empty():
    # Create a mock game state with a knight in a specific position
    mock_gs = MagicMock(spec=game_state)
    mock_gs.board = [[-9 for i in range(8)] for i in range(8)]
    knight = Piece.Knight("white_k", 3, 4, Player.PLAYER_1)
    mock_gs.board[3][4] = knight

    def get_piece(row, col):
        return mock_gs.board[row][col]

    mock_gs.get_piece.side_effect = get_piece
    return mock_gs


@pytest.fixture
def mock_game_state_half(mock_game_state_empty):
    mock_game_state_empty.board[1][3] = Piece.Queen("black_q", 1, 3, Player.PLAYER_2)
    mock_game_state_empty.board[4][2] = Piece.Rook("white_r", 4, 2, Player.PLAYER_1)
    return mock_game_state_empty


@pytest.fixture
def mock_game_state_full(mock_game_state_empty):
    for row, col in [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]:
        mock_game_state_empty.board[row][col] = Piece.Pawn(f"black_p_{row}{col}", row, col, Player.PLAYER_2)
    return mock_game_state_empty


def test_get_valid_peaceful_moves_all_moves(mock_game_state_empty):
    knight = mock_game_state_empty.board[3][4]
    moves = knight.get_valid_peaceful_moves(mock_game_state_empty)
    # Assert that the moves are correct
    assert moves == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]


def test_get_valid_peaceful_moves_some_moves(mock_game_state_half):
    mock_game_state_half.board[3][4] = -9
    knight = Piece.Knight("white_k",0,0,Player.PLAYER_1)
    mock_game_state_half.board[0][0]= knight
    moves = knight.get_valid_peaceful_moves(mock_game_state_half)
    # Assert that the moves are correct
    assert moves == [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, 1), (2, -1)]


def test_get_valid_peaceful_moves_no_moves(mock_game_state_full):
    knight = mock_game_state_full.board[3][4]
    moves = knight.get_valid_peaceful_moves(mock_game_state_full)
    # Assert that the moves are correct
    assert moves == []
