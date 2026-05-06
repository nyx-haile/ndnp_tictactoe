# N-dimensional N-player Tic-tac-toe

Local Python/NumPy implementation of a hypercube tic-tac-toe engine with a small CLI demo.

## Rules

- Defaults are 2 players, 2 dimensions, side length 3, and win length 3.
- The board is an N-dimensional hypercube backed by NumPy.
- Empty cells are `0`; players are numbered `1..N`.
- A win is any contiguous line of `k` marks in any grid direction generated from `-1`, `0`, and `1` direction vectors, excluding the zero vector and duplicate opposites.
- Engine actions are flat integer indices. CLI moves are N-dimensional coordinates that are converted to flat actions.

## CLI

Run the default game:

```bash
python game.py
```

Run a custom 3-player 3D game on a 4x4x4 board where 3 in a row wins:

```bash
python game.py --players 3 --dimensions 3 --side-length 4 --win-length 3
```

At each prompt, enter coordinates separated by spaces or commas, such as `0 1` for the default 2D game or `0,1,2` for a 3D game. Type `board` to print the current board without consuming the turn.

## Engine API

```python
from engine import TicTacToeND

game = TicTacToeND(players=2, dimensions=2, side_length=3, win_length=3)
action = game.coord_to_action((0, 0))
result = game.apply(action)

print(result.current_player)
print(result.legal_actions)
print(result.terminal, result.winner, result.draw)
print(result.returns)
```

Invalid actions and coordinates raise `InvalidMoveError`. The CLI catches those exceptions and asks the same player to retry.

## Tests

Install the minimal dependencies if needed, then run pytest:

```bash
python -m pip install -r requirements.txt
pytest
```

## Scope

This v1 intentionally does not include networking, NDN integration, reinforcement learning training, packaging polish, web UI, or GUI support.
