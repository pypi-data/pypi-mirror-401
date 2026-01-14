"""
Base model configuration for chess-schema.

This module provides the foundational BaseModel that all chess-schema
models inherit from. It's optimized for LLM output parsing with strict
validation to catch hallucinated fields.
"""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ChessBaseModel(BaseModel):
    """
    Base model for all chess-schema models.

    This base class configures Pydantic models to be LLM-friendly while
    maintaining strict validation for reliable parsing in chess analysis
    pipelines.

    Features:
    ---------
    Strict Validation (extra="forbid"):
        Rejects any fields not defined in the schema. This catches LLM
        hallucinations that would otherwise pollute your data pipeline.

    Dual Casing (alias_generator=to_camel, populate_by_name=True):
        - Python code uses snake_case: `game.initial_fen`
        - JSON/LLM uses camelCase: `{"initialFen": "..."}`
        Both formats are accepted during parsing for flexibility.

    Auto-cleanup (str_strip_whitespace=True):
        Automatically strips leading/trailing whitespace from LLM outputs,
        preventing issues like " e4 " != "e4" in move parsing.

    Mutable with Validation (validate_assignment=True):
        Allows post-processing updates (e.g., adding analysis data) while
        re-validating to maintain data integrity.

    Example:
    --------
    >>> from chess_schema import Game
    >>> # LLM returns camelCase JSON
    >>> game = Game.model_validate_json('{"id": "abc", "initialFen": "..."}')
    >>> # Python uses snake_case
    >>> print(game.initial_fen)
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    """

    model_config = ConfigDict(
        # Strict validation: reject undefined fields (catches LLM hallucinations)
        extra="forbid",
        # Auto-strip whitespace from LLM outputs
        str_strip_whitespace=True,
        # Generate camelCase aliases for JSON serialization (LLM-friendly)
        alias_generator=to_camel,
        # Accept both snake_case (Python) and camelCase (JSON/LLM) field names
        populate_by_name=True,
        # Re-validate when fields are modified after instantiation
        validate_assignment=True,
    )
