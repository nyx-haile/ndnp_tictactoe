import pytest

from engine import InvalidMoveError, TicTacToeND


def play_moves(game, moves):
    result = game.result()
    for move in moves:
        result = game.apply(game.coord_to_action(move))
    return result


def test_flat_action_coordinate_round_trip_3d():
    game = TicTacToeND(players=2, dimensions=3, side_length=4, win_length=3)

    for action in (0, 1, 5, 17, 42, 63):
        coordinate = game.action_to_coord(action)
        assert game.coord_to_action(coordinate) == action

    assert game.action_to_coord(23) == (1, 1, 3)
    assert game.coord_to_action((2, 0, 1)) == 33


@pytest.mark.parametrize(
    "winning_moves",
    [
        [(0, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ],
)
def test_2d_row_column_and_diagonal_wins(winning_moves):
    game = TicTacToeND()
    moves = [winning_moves[0], (1, 2), winning_moves[1], (2, 1), winning_moves[2]]

    result = play_moves(game, moves)

    assert result.terminal is True
    assert result.winner == 1
    assert result.draw is False
    assert result.winning_line == tuple(winning_moves)
    assert result.returns == (1.0, -1.0)


@pytest.mark.parametrize(
    "winning_moves",
    [
        [(0, 1, 1), (1, 1, 1), (2, 1, 1)],
        [(0, 0, 2), (1, 1, 2), (2, 2, 2)],
        [(0, 0, 0), (1, 1, 1), (2, 2, 2)],
    ],
)
def test_3d_axis_face_diagonal_and_body_diagonal_wins(winning_moves):
    game = TicTacToeND(players=2, dimensions=3, side_length=3, win_length=3)
    fillers = [(0, 0, 1), (0, 1, 0)]
    moves = [winning_moves[0], fillers[0], winning_moves[1], fillers[1], winning_moves[2]]

    result = play_moves(game, moves)

    assert result.terminal is True
    assert result.winner == 1
    assert result.winning_line == tuple(winning_moves)


def test_4d_axis_win():
    game = TicTacToeND(players=2, dimensions=4, side_length=3, win_length=3)

    result = play_moves(
        game,
        [
            (0, 1, 1, 1),
            (0, 0, 0, 1),
            (1, 1, 1, 1),
            (0, 0, 1, 0),
            (2, 1, 1, 1),
        ],
    )

    assert result.terminal is True
    assert result.winner == 1
    assert result.winning_line == ((0, 1, 1, 1), (1, 1, 1, 1), (2, 1, 1, 1))


def test_4d_mixed_direction_win():
    game = TicTacToeND(players=2, dimensions=4, side_length=3, win_length=3)

    result = play_moves(
        game,
        [
            (0, 1, 2, 0),
            (0, 0, 0, 0),
            (1, 1, 1, 1),
            (0, 0, 0, 1),
            (2, 1, 0, 2),
        ],
    )

    assert result.terminal is True
    assert result.winner == 1
    assert result.winning_line == ((0, 1, 2, 0), (1, 1, 1, 1), (2, 1, 0, 2))


def test_three_player_game_player_three_can_win():
    game = TicTacToeND(players=3, dimensions=2, side_length=4, win_length=3)

    result = play_moves(
        game,
        [
            (1, 0),
            (1, 1),
            (0, 0),
            (2, 0),
            (2, 1),
            (0, 1),
            (3, 1),
            (3, 2),
            (0, 2),
        ],
    )

    assert result.terminal is True
    assert result.winner == 3
    assert result.winning_line == ((0, 0), (0, 1), (0, 2))
    assert result.returns == (-1.0, -1.0, 1.0)


def test_draw_full_board_without_winner():
    game = TicTacToeND(players=2, dimensions=2, side_length=2, win_length=3)
    result = play_moves(game, [(0, 0), (0, 1), (1, 0), (1, 1)])

    assert result.terminal is True
    assert result.draw is True
    assert result.winner is None
    assert result.winning_line == ()
    assert result.returns == (0.0, 0.0)
    assert result.legal_actions == ()


def test_invalid_moves_raise_clear_exceptions():
    game = TicTacToeND()
    game.apply(game.coord_to_action((0, 0)))

    with pytest.raises(InvalidMoveError, match="occupied"):
        game.apply(game.coord_to_action((0, 0)))

    with pytest.raises(InvalidMoveError, match="out of range"):
        game.apply(9)

    with pytest.raises(InvalidMoveError, match="2 dimensions"):
        game.coord_to_action((0, 0, 0))

    with pytest.raises(InvalidMoveError, match="out of bounds"):
        game.coord_to_action((3, 0))


def test_terminal_game_rejects_more_moves():
    game = TicTacToeND()
    play_moves(game, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)])

    with pytest.raises(InvalidMoveError, match="terminal"):
        game.apply(game.coord_to_action((2, 2)))


def test_result_exposes_current_player_and_legal_actions():
    game = TicTacToeND()
    start = game.result()

    assert start.current_player == 1
    assert len(start.legal_actions) == 9

    after_one = game.apply(game.coord_to_action((1, 1)))

    assert after_one.current_player == 2
    assert len(after_one.legal_actions) == 8
    assert game.step(game.coord_to_action((0, 0))).current_player == 1
