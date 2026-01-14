"""
chess-schema: Pydantic models for structured chess game data.

A public library for parsing and validating chess game data in Python,
optimized for LLM output and analysis pipelines. Provides clean, type-safe
models with dual snake_case/camelCase support.

Features:
---------
- Strict validation to catch LLM hallucinations
- UCI + SAN dual notation for moves
- Rich metadata and commentary support
- Recursive variation trees for analysis
- JSON-serializable with Pydantic v2

Basic Usage:
------------
>>> from chess_schema import Game, Player, Move, GameResult, Termination
>>> from datetime import date
>>>
>>> game = Game(
...     id="example_001",
...     white=Player(name="Alice", rating=1800),
...     black=Player(name="Bob", rating=1750),
...     moves=[
...         Move(uci="e2e4", san="e4", ply=1),
...         Move(uci="e7e5", san="e5", ply=2),
...     ],
...     result=GameResult.DRAW,
...     termination=Termination.NORMAL,
...     metadata={"date": date(2024, 1, 13), "event": "Club Championship"}
... )
>>> print(game.model_dump_json(indent=2, by_alias=True))  # camelCase output

LLM Integration:
----------------
Use Field descriptions to guide LLM outputs:

>>> # In your LLM prompt:
>>> # "Return chess game data matching this schema:"
>>> # {Game.model_json_schema()}
>>>
>>> # Parse LLM response:
>>> llm_output = '{"id": "game1", "white": {...}, ...}'
>>> game = Game.model_validate_json(llm_output)

Installation:
-------------
pip install chess-schema

Documentation:
--------------
https://github.com/yourusername/chess-schema
"""

from .base import ChessBaseModel
from .enums import Color, GameResult, Termination
from .game import Game, GameMetadata, Player
from .move import Comment, Move

__version__ = "0.1.3"

# Define public API
__all__ = [
    # Base
    "ChessBaseModel",
    # Enums
    "Color",
    "GameResult",
    "Termination",
    # Game models
    "Game",
    "GameMetadata",
    "Player",
    # Move models
    "Move",
    "Comment",
    # Version
    "__version__",
]
