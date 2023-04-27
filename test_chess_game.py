import pytest
from unittest.mock import MagicMock
from chess_engine import game_state
import Piece
from enums import Player
from ai_engine import chess_ai


#
@pytest.fixture
def mock_game_state_empty():
    """Create a mock game state with empty board and a knight in a specific position"""
    mock_gs = MagicMock(spec=game_state)
    mock_gs.board = [[-9 for i in range(8)] for i in range(8)]
    knight = Piece.Knight("n", 3, 4, Player.PLAYER_1)
    mock_gs.board[3][4] = knight

    # define the mock behaviour
    def get_piece(row, col):
        return mock_gs.board[row][col]

    def is_valid_piece(row, col):
        evaluated_piece = get_piece(row, col)
        return (evaluated_piece is not None) and (evaluated_piece != Player.EMPTY)

    mock_gs.is_valid_piece.side_effect = is_valid_piece
    mock_gs.get_piece.side_effect = get_piece
    return mock_gs


@pytest.fixture
def mock_game_state_full(mock_game_state_empty):
    """Create a mock game state with board and a knight in a specific position surrounded by eight pawns
    in all its legal moves positions"""
    for row, col in [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]:
        mock_game_state_empty.board[row][col] = Piece.Pawn("p", row, col, Player.PLAYER_2)
    return mock_game_state_empty


# board is empty - all 8 legal moves should be returned
def test_get_valid_peaceful_moves_all_moves(mock_game_state_empty):
    knight = mock_game_state_empty.board[3][4]
    moves = knight.get_valid_peaceful_moves(mock_game_state_empty)
    # Assert that the moves are correct
    assert moves == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]


# knight is in the corner ,and one legal cell contains a pawn -
def test_get_valid_peaceful_moves_corner(mock_game_state_empty):
    gs = mock_game_state_empty
    gs.board[3][4] = -9
    knight = Piece.Knight("n", 0, 0, Player.PLAYER_1)
    gs.board[0][0] = knight
    gs.board[1][2] = Piece.Pawn('p', 1, 2, Player.PLAYER_2)
    moves = knight.get_valid_peaceful_moves(gs)
    # Assert that the moves are correct
    assert moves == [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (2, 1), (2, -1)]


# all possible moves have a pawn, no peaceful moves
def test_get_valid_peaceful_moves_no_moves(mock_game_state_full):
    knight = mock_game_state_full.board[3][4]
    moves = knight.get_valid_peaceful_moves(mock_game_state_full)
    # Assert that the moves are correct
    assert moves == []


# all possible moves have a pawn - all moves are valid take moves.
def test_get_valid_piece_takes_all_moves(mock_game_state_full):
    knight = mock_game_state_full.board[3][4]
    moves = knight.get_valid_piece_takes(mock_game_state_full)
    # Assert that the moves are correct
    assert moves == [(1, 3), (1, 5), (2, 2), (2, 6), (4, 2), (4, 6), (5, 5), (5, 3)]


# some possible moves have a pawn from the same color - not all moves are valid take moves.
def test_get_valid_piece_takes_own_pieces(mock_game_state_full):
    gs = mock_game_state_full
    knight = gs.board[3][4]
    gs.board[1][3] = -9
    gs.board[1][3] = Piece.Pawn("p", 1, 3, Player.PLAYER_1)
    gs.board[2][6] = -9
    gs.board[2][6] = Piece.Pawn("p", 1, 3, Player.PLAYER_1)
    moves = knight.get_valid_piece_takes(gs)
    # Assert that the moves are correct
    assert moves == [(1, 5), (2, 2), (4, 2), (4, 6), (5, 5), (5, 3)]


# no opposition pieces in possible moves - no valid take moves.
def test_get_valid_piece_takes_no_moves(mock_game_state_empty):
    knight = mock_game_state_empty.board[3][4]
    moves = knight.get_valid_piece_takes(mock_game_state_empty)
    # Assert that the moves are correct
    assert moves == []


# test get_valid_piece_moves() in Knight class.
def test_integration_get_valid_piece_moves(mock_game_state_empty):
    gs = mock_game_state_empty
    knight = gs.board[3][4]
    gs.board[1][3] = Piece.Pawn("p", 1, 3, Player.PLAYER_2)
    gs.board[2][6] = Piece.Pawn("p", 1, 3, Player.PLAYER_2)
    gs.board[4][2] = Piece.Pawn("p", 1, 3, Player.PLAYER_1)
    moves = knight.get_valid_piece_moves(gs)
    assert moves == [(1, 5), (2, 2), (4, 6), (5, 5), (5, 3), (1, 3), (2, 6)]


# test evaluate_board() in chess_ai class.
def test_integration_evaluate_board(mock_game_state_full):
    gs = mock_game_state_full
    gs.board[0][0] = Piece.Queen("q", 0, 0, Player.PLAYER_2)
    ai_simulator = chess_ai()
    board_value = ai_simulator.evaluate_board(gs, Player.PLAYER_1)
    assert board_value == 150


# system test - check that stupid mat ends game and tha black player won.
def test_system_stupid_mat():
    gs = game_state()
    gs.move_piece((1, 2), (2, 2), False)
    gs.move_piece((6, 3), (4, 3), False)
    gs.move_piece((1, 1), (3, 1), False)
    gs.move_piece((7, 4), (3, 0), False)
    assert gs.checkmate_stalemate_checker() == 0
