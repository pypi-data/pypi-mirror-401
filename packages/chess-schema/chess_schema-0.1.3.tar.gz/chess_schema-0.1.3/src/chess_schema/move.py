"""
Chess move representation with commentary and variations.

This module defines the core Move model used throughout chess-schema.
Moves support both UCI (machine-readable) and SAN (human-readable) formats,
plus recursive variations for analysis trees.
"""

from __future__ import annotations  # Enables forward references for recursive types
from typing import Optional

from pydantic import Field, field_validator

from .base import ChessBaseModel


class Comment(ChessBaseModel):
    """
    A commentary annotation on a move or position.

    Comments can come from various sources (annotators, engines, etc.) and
    are tracked separately to preserve attribution in multi-source analysis.

    Attributes:
    -----------
    text : str
        The actual commentary content. Can be natural language or symbolic
        annotations (e.g., "White has a decisive advantage", "!!", "$14").
    source : str, default="unknown"
        The author or origin of the comment (e.g., "Stockfish 16", "GM Carlsen",
        "lichess_analysis"). Defaults to "unknown" for backwards compatibility.

    Examples:
    ---------
    >>> Comment(text="Brilliant move!", source="GM Nakamura")
    >>> Comment(text="Blunder allows checkmate in 3", source="Stockfish 16")
    """

    text: str = Field(
        description="The actual commentary content (natural language or chess symbols)."
    )
    source: str = Field(
        default="unknown",
        description="The author or origin of the comment (e.g., 'Stockfish 16', 'GM Carlsen').",
    )


class Move(ChessBaseModel):
    """
    Represents a single chess move with optional annotations.

    Moves are stored in dual notation (UCI + SAN) to support both programmatic
    parsing and human readability. Optional fields enable rich annotations like
    comments, variations, and position snapshots.

    Attributes:
    -----------
    uci : str
        Universal Chess Interface notation (e.g., 'e2e4', 'e7e8q'). This is the
        canonical move identifier—unambiguous, parseable, and board-agnostic.
        Promotions append the piece letter (q/r/b/n).
    san : str
        Standard Algebraic Notation (e.g., 'e4', 'Nf3', 'O-O'). Human-readable
        and contextual (requires board state to parse). Useful for display and
        traditional chess notation.
    ply : int, optional
        Half-move number (ply count). 1 = White's first move, 2 = Black's first
        move, etc. Useful for indexing and clock calculations.
    fen : str, optional
        Forsyth-Edwards Notation string representing the board position AFTER
        this move is played. Enables stateless position reconstruction.
    comments : list[Comment], default=[]
        Annotations from humans or engines. Multiple sources can comment on the
        same move (e.g., both a GM and an engine).
    variations : list[list[Move]], default=[]
        Alternative move sequences (sub-variations). Each variation is a list
        of Move objects representing a branching line of play. Enables full
        analysis tree representation.

    Notes:
    ------
    - UCI format is validated for basic structure (4-5 characters, valid squares).
    - The variations field creates a recursive structure that must be resolved
      with `model_rebuild()` after class definition.

    Examples:
    ---------
    >>> move = Move(uci="e2e4", san="e4", ply=1)
    >>> move.comments.append(Comment(text="King's Pawn Opening", source="ECO"))
    >>> # Add a variation exploring 1...e5 instead
    >>> alt = Move(uci="e7e5", san="e5", ply=2)
    >>> move.variations.append([alt])
    """

    uci: str = Field(
        description=(
            "Universal Chess Interface format (e.g., 'e2e4', 'e7e8q'). "
            "Unique, unambiguous, and parseable. Promotions append piece letter."
        ),
    )
    san: str = Field(
        description=(
            "Standard Algebraic Notation (e.g., 'e4', 'Nf3', 'O-O-O'). "
            "Human-readable and context-dependent."
        )
    )
    ply: Optional[int] = Field(
        None,
        description="Half-move number (1 = White's first move, 2 = Black's first move).",
    )
    fen: Optional[str] = Field(
        None,
        description=(
            "FEN string representing the position AFTER this move is played. "
            "Enables stateless position reconstruction."
        ),
    )
    comments: list[Comment] = Field(
        default_factory=list,
        description="List of commentary annotations from various sources (humans, engines).",
    )
    variations: list[list[Move]] = Field(
        default_factory=list,
        description=(
            "Alternative move sequences (sub-variations). Each variation is a "
            "list of Move objects representing a branching analysis line."
        ),
    )

    @field_validator("uci")
    @classmethod
    def validate_uci_format(cls, v: str) -> str:
        """
        Validate UCI move format.

        Ensures the UCI string follows basic structural rules:
        - Length 4 (normal move) or 5 (promotion)
        - First 2 chars are valid square (a-h, 1-8)
        - Next 2 chars are valid square
        - Optional 5th char is promotion piece (q/r/b/n)

        This is a basic sanity check—it doesn't verify move legality.

        Raises:
        -------
        ValueError
            If UCI format is invalid.
        """
        if not (4 <= len(v) <= 5):
            raise ValueError(f"UCI must be 4-5 characters, got '{v}'")

        # Validate source square (chars 0-1)
        if not (v[0] in "abcdefgh" and v[1] in "12345678"):
            raise ValueError(f"Invalid source square in UCI '{v}'")

        # Validate target square (chars 2-3)
        if not (v[2] in "abcdefgh" and v[3] in "12345678"):
            raise ValueError(f"Invalid target square in UCI '{v}'")

        # Validate promotion piece if present (char 4)
        if len(v) == 5 and v[4] not in "qrbn":
            raise ValueError(f"Invalid promotion piece in UCI '{v}', must be q/r/b/n")

        return v


# CRITICAL: Resolve forward reference for recursive variations field
# This must be called after the Move class is fully defined
Move.model_rebuild()
