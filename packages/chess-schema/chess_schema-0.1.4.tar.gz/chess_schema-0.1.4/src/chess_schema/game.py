"""
Complete chess game representation with metadata and moves.

This module defines the top-level Game model that ties together players,
metadata, moves, and game outcomes into a single validated structure.
Includes PGN parsing for easy conversion from standard chess notation.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional, Union, Any
from datetime import date as DateType
import uuid

from pydantic import Field, HttpUrl, field_validator

from .base import ChessBaseModel
from .enums import GameResult, Termination, get_termination_docstring
from .move import Move, Comment


# Standard starting position for chess games
_STANDARD_STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Player(ChessBaseModel):
    """
    Represents a player in a chess game.

    Stores player identification and rating information. Title is optional
    to support both titled and untitled players.

    Attributes:
    -----------
    name : str
        Player's username or real name (e.g., "DrNykterstein", "Magnus Carlsen").
    rating : int, optional
        Player's rating at time of game (e.g., Elo, FIDE, Lichess, Chess.com rating).
    title : str, optional
        Player's title if any (e.g., "GM", "IM", "FM", "WGM", "NM").

    Examples:
    ---------
    >>> Player(name="Magnus Carlsen", rating=2830, title="GM")
    >>> Player(name="AnonymousPlayer123", rating=1500)  # No title
    """

    name: str = Field(
        description="Player's username or real name (e.g., 'DrNykterstein', 'Magnus Carlsen')."
    )
    rating: Optional[int] = Field(
        None,
        description="Player's rating at game time (Elo, FIDE, Lichess, Chess.com).",
        ge=0,  # Rating cannot be negative
        le=4000,  # Sanity check: highest ratings are ~2900
    )
    title: Optional[str] = Field(
        None,
        description="Player's title if any (e.g., 'GM', 'IM', 'FM', 'WGM', 'NM').",
    )


class GameMetadata(ChessBaseModel):
    """
    Metadata about a chess game.

    Stores contextual information about when/where the game was played and
    how to categorize it. All fields are optional to support partial data.

    Attributes:
    -----------
    event : str, optional
        Tournament or match name (e.g., "World Chess Championship 2024", "Titled Tuesday").
    site : str, optional
        Location or platform where game was played (e.g., "Dubai, UAE", "lichess.org").
    date : date | str | None, optional
        Date the game was played. Accepts:
        - Python date objects for known dates
        - PGN format strings for partial dates (e.g., "2024.01.??" if day unknown)
        - None if date is completely unknown
    round : str, optional
        Round number or identifier (e.g., "1", "Final", "1.3" for round 1, board 3).
    source_url : HttpUrl, optional
        Direct link to the game (e.g., "https://lichess.org/abc123").
    tags : list[str], default=[]
        Custom tags for categorization (e.g., ["blitz", "sicilian_defense", "time_scramble"]).

    Examples:
    ---------
    >>> from datetime import date
    >>> GameMetadata(
    ...     event="World Chess Championship 2024",
    ...     site="Dubai, UAE",
    ...     date=date(2024, 11, 25),
    ...     round="1",
    ...     source_url="https://chess.com/game123"
    ... )
    """

    event: Optional[str] = Field(
        None,
        description="Tournament or match name (e.g., 'World Chess Championship 2024').",
    )
    site: Optional[str] = Field(
        None,
        description="Location or platform where game was played (e.g., 'Dubai, UAE', 'lichess.org').",
    )
    date: Union[DateType, str, None] = Field(
        None,
        description=(
            "Date game was played. Use Python date for known dates, "
            "PGN format 'YYYY.MM.??' for partial dates, or None if unknown."
        ),
    )
    round: Optional[str] = Field(
        None,
        description="Round number or identifier (e.g., '1', 'Final', '1.3').",
    )
    source_url: Optional[HttpUrl] = Field(
        None,
        description="Direct URL to the game (e.g., 'https://lichess.org/abc123').",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Custom tags for categorization (e.g., ['blitz', 'sicilian_defense']).",
    )


class Game(ChessBaseModel):
    """
    Complete representation of a chess game.

    This is the top-level model that brings together all components: players,
    metadata, moves, and outcome. It's designed to be both LLM-friendly (with
    clear field descriptions) and pipeline-ready (with strict validation).

    Attributes:
    -----------
    id : str
        Unique game identifier. Use UUID for internal games or platform-specific
        IDs for Lichess/Chess.com games (e.g., "abc12345", "uuid-v4-string").
    metadata : GameMetadata
        Contextual information about the game (event, site, date, etc.).
    initial_fen : str, default=standard starting position
        FEN string for the starting position. Defaults to standard chess starting
        position but can be set for Chess960 or custom positions.
    white : Player
        White player information.
    black : Player
        Black player information.
    moves : list[Move], default=[]
        Ordered list of all moves played in the game (mainline). Each Move can
        contain variations for analysis branches.
    result : GameResult
        Final game outcome ("1-0", "0-1", "1/2-1/2", or "*").
    termination : Termination
        Specific reason for game ending (e.g., "normal", "time forfeit").

    Notes:
    ------
    - The `id` field should be unique across your entire dataset to prevent
      duplicate game imports.
    - For Chess960/Fischer Random, set `initial_fen` to the actual starting
      position and ensure moves use Chess960 castling notation.
    - Moves are validated individually, but move legality is NOT checked—
      that's the responsibility of your game parser/generator.

    Examples:
    ---------
    >>> from datetime import date
    >>> game = Game(
    ...     id="lichess_abc123",
    ...     metadata=GameMetadata(
    ...         event="Titled Tuesday",
    ...         site="lichess.org",
    ...         date=date(2024, 1, 13)
    ...     ),
    ...     white=Player(name="PlayerA", rating=2400),
    ...     black=Player(name="PlayerB", rating=2380),
    ...     moves=[
    ...         Move(uci="e2e4", san="e4", ply=1),
    ...         Move(uci="e7e5", san="e5", ply=2)
    ...     ],
    ...     result=GameResult.WHITE_WIN,
    ...     termination=Termination.NORMAL
    ... )
    """

    id: str = Field(
        description=(
            "Unique game identifier (UUID or platform-specific ID like 'lichess_abc123'). "
            "Must be unique across your dataset."
        )
    )
    metadata: GameMetadata = Field(
        description="Contextual information about the game (event, site, date, etc.)."
    )
    initial_fen: str = Field(
        default=_STANDARD_STARTING_FEN,
        description=(
            "FEN string for the starting position. Defaults to standard chess "
            "starting position. Override for Chess960 or custom positions."
        ),
    )
    white: Player = Field(description="White player information.")
    black: Player = Field(description="Black player information.")
    moves: list[Move] = Field(
        default_factory=list,
        description="Ordered list of all moves played (mainline with optional variations).",
    )
    result: GameResult = Field(
        description="Final game outcome ('1-0', '0-1', '1/2-1/2', or '*' for unterminated)."
    )
    termination: Termination = Field(description=get_termination_docstring())

    @field_validator("initial_fen")
    @classmethod
    def validate_fen_structure(cls, v: str) -> str:
        """
        Validate basic FEN structure.

        Performs lightweight validation to catch obviously malformed FENs:
        - Must have 6 space-separated fields
        - First field (board) must have 8 ranks separated by '/'

        Does NOT validate:
        - Piece placement correctness (e.g., two kings)
        - Move legality
        - Positional impossibilities

        Raises:
        -------
        ValueError
            If FEN structure is invalid.
        """
        parts = v.split()
        if len(parts) != 6:
            raise ValueError(
                f"FEN must have 6 space-separated fields, got {len(parts)}: '{v}'"
            )

        board_part = parts[0]
        ranks = board_part.split("/")
        if len(ranks) != 8:
            raise ValueError(
                f"FEN board must have 8 ranks separated by '/', got {len(ranks)}: '{board_part}'"
            )

        return v

    @field_validator("moves")
    @classmethod
    def validate_move_plies(cls, v: list[Move]) -> list[Move]:
        """
        Validate move ply numbers are sequential if provided.

        If ply numbers are set on moves, ensures they increment correctly
        (1, 2, 3, ...). Skips validation if any move lacks a ply number.

        Raises:
        -------
        ValueError
            If ply numbers are non-sequential.
        """
        if not v:  # Empty move list is valid
            return v

        # Only validate if all moves have ply numbers
        if all(move.ply is not None for move in v):
            for i, move in enumerate(v):
                expected_ply = i + 1
                if move.ply != expected_ply:
                    raise ValueError(
                        f"Move {i} has ply={move.ply}, expected ply={expected_ply}. "
                        f"Ply numbers must be sequential starting from 1."
                    )

        return v

    @classmethod
    def from_pgn(
        cls,
        pgn_string: str,
        *,
        game_id: Optional[str] = None,
        require_chess_library: bool = False,
    ) -> Game:
        """
        Parse a PGN string into a Game object.

        This method converts standard PGN notation into a validated Game model.
        It extracts headers, moves, comments, and variations while generating
        UCI notation for reliable programmatic access.

        Parameters:
        -----------
        pgn_string : str
            Complete PGN game string including headers and movetext.
        game_id : str, optional
            Override the game ID. If not provided, generates a UUID or uses
            the "Site" tag if it looks like a game URL.
        require_chess_library : bool, default=False
            If True, raises ImportError if python-chess is not installed.
            If False (default), raises a helpful error suggesting installation.

        Returns:
        --------
        Game
            Validated Game object with all data extracted from PGN.

        Raises:
        -------
        ImportError
            If python-chess library is not installed.
        ValueError
            If PGN is malformed or cannot be parsed.

        Notes:
        ------
        This method requires the `python-chess` library to parse PGN and
        generate UCI notation. Install it with:
            pip install python-chess

        The parser attempts to extract:
        - All standard PGN headers (Event, Site, Date, Round, White, Black, etc.)
        - Player ratings from WhiteElo/BlackElo tags
        - Player titles from WhiteTitle/BlackTitle tags
        - Game result and termination reason
        - All moves with SAN and UCI notation
        - Move comments and variations (if present)
        - Initial FEN for non-standard positions

        Examples:
        ---------
        >>> pgn = '''
        ... [Event "World Championship"]
        ... [Site "Dubai"]
        ... [Date "2024.01.13"]
        ... [Round "1"]
        ... [White "Carlsen, Magnus"]
        ... [Black "Nepomniachtchi, Ian"]
        ... [Result "1-0"]
        ... [WhiteElo "2830"]
        ... [BlackElo "2795"]
        ...
        ... 1. e4 e5 2. Nf3 Nc6 3. Bb5 1-0
        ... '''
        >>> game = Game.from_pgn(pgn)
        >>> print(game.white.name)
        'Carlsen, Magnus'
        >>> print(game.moves[0].uci)
        'e2e4'

        >>> # With custom ID
        >>> game = Game.from_pgn(pgn, game_id="custom_id_001")
        """
        try:
            import chess.pgn
            import io
        except ImportError as e:
            if require_chess_library:
                raise
            raise ImportError(
                "The 'python-chess' library is required to parse PGN files. "
                "Install it with: pip install python-chess"
            ) from e

        # Parse PGN using python-chess
        pgn_io = io.StringIO(pgn_string)
        try:
            parsed_game = chess.pgn.read_game(pgn_io)
        except Exception as e:
            raise ValueError(f"Failed to parse PGN: {e}") from e

        if parsed_game is None:
            raise ValueError("PGN string is empty or contains no valid game")

        # Extract headers
        headers = parsed_game.headers

        # Generate or extract game ID
        final_game_id: str
        if game_id is None:
            # Try to extract ID from Site tag if it looks like a URL
            site = headers.get("Site", "")
            if "/" in site and any(
                domain in site for domain in ["lichess", "chess.com"]
            ):
                # Extract last part of URL as ID
                final_game_id = site.rstrip("/").split("/")[-1]
            else:
                # Generate UUID
                final_game_id = str(uuid.uuid4())
        else:
            final_game_id = game_id

        # Parse date
        date_str = headers.get("Date", "????.??.??")
        parsed_date: Union[DateType, str, None] = None
        if date_str and date_str != "????.??.??":
            try:
                # Try to parse as full date
                parsed_date = datetime.strptime(date_str, "%Y.%m.%d").date()
            except ValueError:
                # Keep as string if partial date (e.g., "2024.01.??")
                parsed_date = date_str
        else:
            parsed_date = None

        # Extract player info
        white = Player(
            name=headers.get("White", "Unknown"),
            rating=int(headers["WhiteElo"]) if headers.get("WhiteElo") else None,
            title=headers.get("WhiteTitle"),
        )
        black = Player(
            name=headers.get("Black", "Unknown"),
            rating=int(headers["BlackElo"]) if headers.get("BlackElo") else None,
            title=headers.get("BlackTitle"),
        )

        # Build metadata
        metadata = GameMetadata(
            event=headers.get("Event"),
            site=headers.get("Site"),
            date=parsed_date,
            round=headers.get("Round"),
            source_url=None,  # HttpUrl validation would fail on non-URL sites
        )

        # Parse result
        result_str = headers.get("Result", "*")
        try:
            result = GameResult(result_str)
        except ValueError:
            result = GameResult.UNTERMINATED

        # Parse termination
        termination_str = headers.get("Termination", "").lower()
        termination = Termination.UNTERMINATED
        for term in Termination:
            if term.value in termination_str:
                termination = term
                break
        # Default to NORMAL for completed games if not specified
        if (
            termination == Termination.UNTERMINATED
            and result != GameResult.UNTERMINATED
        ):
            termination = Termination.NORMAL

        # Get initial position
        initial_fen = headers.get("FEN", _STANDARD_STARTING_FEN)

        # Extract moves with UCI conversion
        moves = cls._extract_moves_from_node(parsed_game, initial_fen)

        return cls(
            id=final_game_id,
            metadata=metadata,
            initial_fen=initial_fen,
            white=white,
            black=black,
            moves=moves,
            result=result,
            termination=termination,
        )

    @staticmethod
    def _extract_moves_from_node(
        node: Any, initial_fen: str, ply_offset: int = 0
    ) -> list[Move]:
        """
        Recursively extract moves from a python-chess game node.

        This helper method traverses the PGN game tree, extracting mainline
        moves and variations while generating UCI notation.

        Parameters:
        -----------
        node : Any (chess.pgn.GameNode when python-chess is installed)
            Current node in the game tree.
        initial_fen : str
            FEN position before the first move.
        ply_offset : int, default=0
            Offset for ply numbering (used in variations).

        Returns:
        --------
        list[Move]
            List of Move objects with UCI, SAN, and variations.
        """
        import chess

        moves: list[Move] = []
        board = chess.Board(initial_fen)
        ply = 1 + ply_offset

        # Traverse mainline
        for move_node in node.mainline():
            chess_move = move_node.move
            san = board.san(chess_move)
            uci = chess_move.uci()

            # Extract comments
            comments = []
            if move_node.comment:
                comments.append(Comment(text=move_node.comment, source="pgn"))

            # Apply move to get resulting FEN
            board.push(chess_move)
            resulting_fen = board.fen()

            # Extract variations
            variations = []
            for variation in move_node.variations[1:]:  # Skip mainline (index 0)
                # Variations start from the position BEFORE this move
                var_board = board.copy()
                var_board.pop()  # Undo the mainline move
                var_moves = Game._extract_moves_from_node(
                    variation.parent,  # Start from parent
                    var_board.fen(),
                    ply_offset=ply - 1,
                )
                # Only include the variation branch (not the mainline move again)
                if var_moves:
                    variations.append(
                        var_moves[1:] if len(var_moves) > 1 else var_moves
                    )

            move_obj = Move(
                uci=uci,
                san=san,
                ply=ply,
                fen=resulting_fen,
                comments=comments,
                variations=variations,
            )
            moves.append(move_obj)
            ply += 1

        return moves
