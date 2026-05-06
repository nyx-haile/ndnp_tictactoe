from __future__ import annotations

import argparse

from engine import InvalidConfigurationError, InvalidMoveError, TicTacToeND


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="N-dimensional N-player tic-tac-toe")
    parser.add_argument("--players", type=int, default=2, help="number of players, default: 2")
    parser.add_argument("--dimensions", type=int, default=2, help="number of board dimensions, default: 2")
    parser.add_argument("--side-length", type=int, default=3, help="hypercube side length, default: 3")
    parser.add_argument("--win-length", type=int, default=3, help="marks in a line required to win, default: 3")
    return parser


def parse_coordinate(text: str, dimensions: int) -> tuple[int, ...]:
    cleaned = text.replace(",", " ").strip()
    parts = cleaned.split()
    if len(parts) != dimensions:
        raise InvalidMoveError(f"coordinate must have {dimensions} dimensions")
    try:
        return tuple(int(part) for part in parts)
    except ValueError as error:
        raise InvalidMoveError("coordinate values must be integers") from error


def print_status(game: TicTacToeND) -> None:
    print("\nBoard:")
    print(game.board)
    print(f"Legal actions: {game.legal_actions()}")


def run_cli(game: TicTacToeND) -> None:
    print("N-dimensional N-player tic-tac-toe")
    print("Enter coordinates separated by spaces or commas, or type 'board' to inspect the board.")
    print_status(game)

    while not game.terminal:
        prompt = f"\nPlayer {game.current_player}, enter {game.dimensions} coordinates: "
        raw_move = input(prompt)
        if raw_move.strip().lower() == "board":
            print_status(game)
            continue

        try:
            coordinate = parse_coordinate(raw_move, game.dimensions)
            action = game.coord_to_action(coordinate)
            result = game.apply(action)
        except InvalidMoveError as error:
            print(f"Invalid move: {error}")
            continue

        print_status(game)
        if result.terminal:
            if result.draw:
                print("Game over: draw.")
            else:
                print(f"Game over: player {result.winner} wins!")
                print(f"Winning line: {result.winning_line}")


def main() -> int:
    args = build_parser().parse_args()
    try:
        game = TicTacToeND(
            players=args.players,
            dimensions=args.dimensions,
            side_length=args.side_length,
            win_length=args.win_length,
        )
    except InvalidConfigurationError as error:
        print(f"Invalid configuration: {error}")
        return 2

    run_cli(game)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
