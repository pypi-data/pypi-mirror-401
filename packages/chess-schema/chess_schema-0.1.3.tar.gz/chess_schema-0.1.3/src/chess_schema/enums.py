"""
Enumerations for chess game outcomes and metadata.

This module defines standard chess enums that LLMs can reliably output
as string values, avoiding ambiguity in game result interpretation.
"""

from enum import Enum
from typing import Dict


class Color(str, Enum):
    """
    Chess piece color.

    String-based enum for compatibility with JSON and LLM outputs.
    Inheriting from str allows direct string comparison and serialization.
    """

    WHITE = "white"
    BLACK = "black"


class GameResult(str, Enum):
    """
    Final game result in standard PGN notation.

    These values match the PGN standard for unambiguous result reporting.
    LLMs should output these exact strings to indicate game outcomes.

    Values:
    -------
    WHITE_WIN : "1-0"
        White wins the game.
    BLACK_WIN : "0-1"
        Black wins the game.
    DRAW : "1/2-1/2"
        Game ends in a draw (stalemate, agreement, insufficient material, etc.).
    UNTERMINATED : "*"
        Game is ongoing or result unknown.
    """

    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"
    DRAW = "1/2-1/2"
    UNTERMINATED = "*"


class Termination(str, Enum):
    """
    Specific reason for game termination.

    Provides granular classification of how/why a game ended, useful for
    filtering and analysis (e.g., studying time pressure losses vs. resignations).

    Based on PGN standard termination tags with common extensions.

    Values:
    -------
    ABANDONED : "abandoned"
        Game was abandoned without completion.
    ADJUDICATION : "adjudication"
        Result determined by arbiter/third-party ruling (common in correspondence chess).
    DEATH : "death"
        Player passed away during the game (historical games).
    EMERGENCY : "emergency"
        Game ended due to unforeseen emergency circumstances.
    NORMAL : "normal"
        Standard game ending (checkmate, resignation, draw agreement, stalemate).
    RULES_INFRACTION : "rules infraction"
        Forfeit due to illegal move or rules violation.
    TIME_FORFEIT : "time forfeit"
        Loss on time (flag fell in timed games).
    UNTERMINATED : "unterminated"
        Game is still in progress or termination unknown.
    """

    ABANDONED = "abandoned"
    ADJUDICATION = "adjudication"
    DEATH = "death"
    EMERGENCY = "emergency"
    NORMAL = "normal"
    RULES_INFRACTION = "rules infraction"
    TIME_FORFEIT = "time forfeit"
    UNTERMINATED = "unterminated"


# Internal mapping for generating LLM-friendly documentation
_TERMINATION_DESCRIPTIONS: Dict[Termination, str] = {
    Termination.ABANDONED: "Abandoned game.",
    Termination.ADJUDICATION: "Result due to third party adjudication process.",
    Termination.DEATH: "Losing player called to greater things, one hopes.",
    Termination.EMERGENCY: "Game concluded due to unforeseen circumstances.",
    Termination.NORMAL: "Game terminated in a normal fashion (checkmate, resignation, draw agreement, stalemate).",
    Termination.RULES_INFRACTION: "Administrative forfeit due to failure to observe Laws of Chess.",
    Termination.TIME_FORFEIT: "Loss due to losing player's failure to meet time control requirements.",
    Termination.UNTERMINATED: "Game not terminated.",
}


def get_termination_docstring() -> str:
    """
    Generate detailed termination documentation for LLM prompts.

    This function creates a formatted string listing all valid termination
    reasons with descriptions, which can be embedded in Pydantic Field
    descriptions to guide LLM outputs.

    Returns:
    --------
    str
        Multi-line string documenting all termination options.

    Example Output:
    ---------------
    Specific termination reason. Options:
    - 'normal': Game terminated in a normal fashion...
    - 'time forfeit': Loss due to losing player's failure...
    ...
    """
    lines = ["Specific termination reason. Options:"]
    for term, desc in _TERMINATION_DESCRIPTIONS.items():
        lines.append(f"- '{term.value}': {desc}")
    return "\n".join(lines)
