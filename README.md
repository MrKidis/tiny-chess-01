# tiny-chess-01 entry

A 4 KB chess engine in Python, entered for make.fun's
[Build the strongest chess engine in 4 KB of Python](https://make.fun/bounty/tiny-chess-01).

![make.fun](https://make.fun/badge/tiny-chess-01.svg)
![rank](https://make.fun/badge/tiny-chess-01/MrKidis/tiny-chess-01/rank.svg)
![reward](https://make.fun/badge/tiny-chess-01/MrKidis/tiny-chess-01/reward.svg)

## The engine

- `main.py` at the repository root is the whole engine: at most 4,096 bytes as
  committed (comments, whitespace and docstrings count).
- Python 3.13 with the standard library only; it reads, imports and execs no
  other file of the repository.
- It talks to the env alone, over HTTP: `POST $MAKEFUN_ENV_URL/game` serves the
  game in play and `POST $MAKEFUN_ENV_URL/move` plays a move.
- It parses the FEN into a 128-square board, generates legal moves, runs an
  alpha-beta search to a fixed depth against the env's own legality answers, and
  picks the best move: a material-plus-pawn-progress heuristic, with in-check
  filtering. The search never reads a clock, so trials replay byte for byte.
- Moves are UCI as the env serves them, promotions as `a7a8q`.
