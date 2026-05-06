from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable

import numpy as np


Coordinate = tuple[int, ...]


class InvalidConfigurationError(ValueError):
    """Raised when game configuration values cannot describe a valid board."""


class InvalidMoveError(ValueError):
    """Raised when an action or coordinate is invalid for the current state."""


@dataclass(frozen=True)
class GameResult:
    winner: int | None
    draw: bool
    terminal: bool
    winning_line: tuple[Coordinate, ...]
    current_player: int | None
    legal_actions: tuple[int, ...]
    returns: tuple[float, ...]


class TicTacToeND:
    def __init__(
        self,
        players: int = 2,
        dimensions: int = 2,
        side_length: int = 3,
        win_length: int = 3,
        board: np.ndarray | None = None,
        current_player: int = 1,
    ):
        self.players = self._positive_int(players, "players")
        self.dimensions = self._positive_int(dimensions, "dimensions")
        self.side_length = self._positive_int(side_length, "side_length")
        self.win_length = self._positive_int(win_length, "win_length")
        self.current_player = self._positive_int(current_player, "current_player")

        if self.players < 2:
            raise InvalidConfigurationError("players must be at least 2")
        if not 1 <= self.current_player <= self.players:
            raise InvalidConfigurationError("current_player must be between 1 and players")

        shape = (self.side_length,) * self.dimensions
        if board is None:
            self.board = np.zeros(shape, dtype=np.int64)
        else:
            if board.shape != shape:
                raise InvalidConfigurationError(f"board shape must be {shape}")
            if np.any((board < 0) | (board > self.players)):
                raise InvalidConfigurationError("board values must be empty=0 or players=1..N")
            self.board = board.astype(np.int64, copy=True)

        self._directions = self._generate_directions(self.dimensions)
        self._occupied = int(np.count_nonzero(self.board))
        self._winner: int | None = None
        self._draw = False
        self._terminal = False
        self._winning_line: tuple[Coordinate, ...] = ()

        if self._occupied == self.board.size:
            self._terminal = True
            self._draw = True

    @staticmethod
    def _positive_int(value: int, name: str) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidConfigurationError(f"{name} must be an integer")
        if value <= 0:
            raise InvalidConfigurationError(f"{name} must be positive")
        return value

    @staticmethod
    def _generate_directions(dimensions: int) -> tuple[Coordinate, ...]:
        directions: list[Coordinate] = []
        for vector in product((-1, 0, 1), repeat=dimensions):
            if all(component == 0 for component in vector):
                continue
            first_nonzero = next(component for component in vector if component != 0)
            if first_nonzero > 0:
                directions.append(tuple(vector))
        return tuple(directions)

    @property
    def shape(self) -> tuple[int, ...]:
        return self.board.shape

    @property
    def terminal(self) -> bool:
        return self._terminal

    def clone(self) -> TicTacToeND:
        clone = TicTacToeND(
            players=self.players,
            dimensions=self.dimensions,
            side_length=self.side_length,
            win_length=self.win_length,
            board=self.board,
            current_player=self.current_player,
        )
        clone._occupied = self._occupied
        clone._winner = self._winner
        clone._draw = self._draw
        clone._terminal = self._terminal
        clone._winning_line = self._winning_line
        return clone

    def action_to_coord(self, action: int) -> Coordinate:
        if isinstance(action, bool) or not isinstance(action, int):
            raise InvalidMoveError("action must be an integer")
        if action < 0 or action >= self.board.size:
            raise InvalidMoveError(f"action out of range: expected 0..{self.board.size - 1}")
        return tuple(int(part) for part in np.unravel_index(action, self.shape))

    def coord_to_action(self, coordinate: Iterable[int]) -> int:
        coordinate = tuple(coordinate)
        if len(coordinate) != self.dimensions:
            raise InvalidMoveError(f"coordinate must have {self.dimensions} dimensions")
        if any(isinstance(part, bool) or not isinstance(part, int) for part in coordinate):
            raise InvalidMoveError("coordinate values must be integers")
        if any(part < 0 or part >= self.side_length for part in coordinate):
            raise InvalidMoveError(f"coordinate out of bounds: each value must be 0..{self.side_length - 1}")
        return int(np.ravel_multi_index(coordinate, self.shape))

    def legal_actions(self) -> tuple[int, ...]:
        if self._terminal:
            return ()
        return tuple(int(action) for action in np.flatnonzero(self.board.ravel() == 0))

    def result(self) -> GameResult:
        return GameResult(
            winner=self._winner,
            draw=self._draw,
            terminal=self._terminal,
            winning_line=self._winning_line,
            current_player=None if self._terminal else self.current_player,
            legal_actions=self.legal_actions(),
            returns=self.returns(),
        )

    def returns(self) -> tuple[float, ...]:
        if not self._terminal or self._draw:
            return (0.0,) * self.players
        return tuple(1.0 if player == self._winner else -1.0 for player in range(1, self.players + 1))

    def apply(self, action: int) -> GameResult:
        if self._terminal:
            raise InvalidMoveError("cannot apply move to terminal game")

        coordinate = self.action_to_coord(action)
        if self.board[coordinate] != 0:
            raise InvalidMoveError(f"cell {coordinate} is already occupied")

        player = self.current_player
        self.board[coordinate] = player
        self._occupied += 1

        winning_line = self._find_winning_line(coordinate, player)
        if winning_line:
            self._winner = player
            self._terminal = True
            self._winning_line = winning_line
        elif self._occupied == self.board.size:
            self._draw = True
            self._terminal = True
        else:
            self.current_player = (self.current_player % self.players) + 1

        return self.result()

    def step(self, action: int) -> GameResult:
        return self.apply(action)

    def _find_winning_line(self, coordinate: Coordinate, player: int) -> tuple[Coordinate, ...]:
        if self.win_length > self.side_length:
            return ()

        for direction in self._directions:
            line = self._line_through(coordinate, direction, player)
            if len(line) >= self.win_length:
                for index, member in enumerate(line):
                    if member == coordinate:
                        start = max(0, min(index, len(line) - self.win_length))
                        return tuple(line[start : start + self.win_length])
        return ()

    def _line_through(self, coordinate: Coordinate, direction: Coordinate, player: int) -> list[Coordinate]:
        negative = self._scan(coordinate, tuple(-part for part in direction), player)
        positive = self._scan(coordinate, direction, player)
        return list(reversed(negative)) + [coordinate] + positive

    def _scan(self, coordinate: Coordinate, direction: Coordinate, player: int) -> list[Coordinate]:
        scanned: list[Coordinate] = []
        current = coordinate
        while True:
            current = tuple(current[index] + direction[index] for index in range(self.dimensions))
            if any(part < 0 or part >= self.side_length for part in current):
                return scanned
            if self.board[current] != player:
                return scanned
            scanned.append(current)
