import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_cli_help_smoke():
    completed = subprocess.run(
        [sys.executable, "game.py", "--help"],
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert completed.returncode == 0
    assert "N-dimensional N-player tic-tac-toe" in completed.stdout
    assert "--players" in completed.stdout


def test_cli_plays_complete_default_game():
    completed = subprocess.run(
        [sys.executable, "game.py"],
        input="0 0\n1 0\n0 1\n1 1\n0 2\n",
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=5,
    )

    assert completed.returncode == 0
    assert "Game over: player 1 wins!" in completed.stdout
    assert "Winning line: ((0, 0), (0, 1), (0, 2))" in completed.stdout
