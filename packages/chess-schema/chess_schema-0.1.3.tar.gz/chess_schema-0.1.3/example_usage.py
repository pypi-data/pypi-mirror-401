"""
Example usage of chess-schema library.

This file demonstrates various ways to create and work with Game objects,
including PGN parsing, manual construction, and JSON serialization.
"""

from chess_schema import (
    Game,
    Player,
    Move,
    Comment,
    GameMetadata,
    GameResult,
    Termination,
)
from datetime import date


def example_from_pgn():
    """Example: Parse a PGN string into a Game object."""
    print("=" * 60)
    print("Example 1: Parsing from PGN")
    print("=" * 60)

    pgn = """
[Event "F/S Return Match"]
[Site "Belgrade, Serbia JUG"]
[Date "1992.11.04"]
[Round "29"]
[White "Fischer, Robert J."]
[Black "Spassky, Boris V."]
[Result "1/2-1/2"]
[WhiteElo "2785"]
[BlackElo "2560"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 
8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 1/2-1/2
"""

    game = Game.from_pgn(pgn)

    print(f"Game ID: {game.id}")
    print(f"Event: {game.metadata.event}")
    print(f"Date: {game.metadata.date}")
    print(f"White: {game.white.name} ({game.white.rating})")
    print(f"Black: {game.black.name} ({game.black.rating})")
    print(f"Result: {game.result.value}")
    print(f"Total moves: {len(game.moves)}")
    print(f"First move: {game.moves[0].san} (UCI: {game.moves[0].uci})")
    print()


def example_manual_construction():
    """Example: Manually construct a Game object."""
    print("=" * 60)
    print("Example 2: Manual Construction")
    print("=" * 60)

    game = Game(
        id="example_manual_001",
        metadata=GameMetadata(
            event="Local Tournament",
            site="New York, USA",
            date=date(2024, 1, 13),
            round="1",
            tags=["blitz", "ruy_lopez"],
        ),
        white=Player(name="Alice", rating=1800, title="NM"),
        black=Player(name="Bob", rating=1750),
        moves=[
            Move(uci="e2e4", san="e4", ply=1),
            Move(uci="e7e5", san="e5", ply=2),
            Move(
                uci="g1f3",
                san="Nf3",
                ply=3,
                comments=[Comment(text="King's Knight Opening", source="opening_book")],
            ),
            Move(uci="b8c6", san="Nc6", ply=4),
        ],
        result=GameResult.WHITE_WIN,
        termination=Termination.NORMAL,
    )

    print(f"Game ID: {game.id}")
    print(f"Event: {game.metadata.event}")
    print(f"Tags: {game.metadata.tags}")
    print(f"Move 3: {game.moves[2].san}")
    print(f"Move 3 comment: {game.moves[2].comments[0].text}")
    print()


def example_with_variations():
    """Example: Parse PGN with variations and comments."""
    print("=" * 60)
    print("Example 3: PGN with Variations and Comments")
    print("=" * 60)

    pgn = """
[Event "Annotated Game"]
[Site "Online"]
[Date "2024.01.13"]
[White "Student"]
[Black "Master"]
[Result "0-1"]

1. e4 { The most popular opening move } e5 
(1... c5 { Sicilian Defense - more aggressive } 2. Nf3 d6)
2. Nf3 Nc6 3. Bc4?! { Dubious - allows strong response } 
(3. Bb5 { Ruy Lopez is better }) 
3... Nf6! { Excellent development } 0-1
"""

    game = Game.from_pgn(pgn)

    print(f"First move: {game.moves[0].san}")
    print(f"Comment: {game.moves[0].comments[0].text}")
    print(f"Has variation: {len(game.moves[0].variations) > 0}")

    if game.moves[0].variations:
        variation = game.moves[0].variations[0]
        print(f"Variation first move: {variation[0].san}")

    print()


def example_json_serialization():
    """Example: Serialize Game to JSON (for LLM integration)."""
    print("=" * 60)
    print("Example 4: JSON Serialization")
    print("=" * 60)

    game = Game(
        id="json_example",
        metadata=GameMetadata(event="Test Event"),
        white=Player(name="White Player", rating=2000),
        black=Player(name="Black Player", rating=1950),
        moves=[
            Move(uci="e2e4", san="e4", ply=1),
            Move(uci="e7e5", san="e5", ply=2),
        ],
        result=GameResult.DRAW,
        termination=Termination.NORMAL,
    )

    # Serialize with camelCase (for LLMs/JSON APIs)
    json_camel = game.model_dump_json(indent=2, by_alias=True)
    print("JSON with camelCase:")
    print(json_camel[:300] + "...")
    print()

    # Serialize with snake_case (Python-style)
    json_snake = game.model_dump_json(indent=2, by_alias=False)
    print("JSON with snake_case:")
    print(json_snake[:300] + "...")
    print()


def example_validation():
    """Example: Show validation errors."""
    print("=" * 60)
    print("Example 5: Validation")
    print("=" * 60)

    # This will raise a validation error
    try:
        Move(uci="invalid", san="e4")
    except Exception as e:
        print(f"❌ Invalid UCI caught: {type(e).__name__}")
        print(f"   {e}")
    print()

    # This will also raise a validation error
    try:
        Game(
            id="test",
            white=Player(name="Alice", rating=5000),  # Invalid rating
            black=Player(name="Bob"),
            result=GameResult.DRAW,
            termination=Termination.NORMAL,
            metadata=GameMetadata(),
        )
    except Exception as e:
        print(f"❌ Invalid rating caught: {type(e).__name__}")
        print(f"   Rating must be <= 4000")
    print()


def example_pgn_to_json_pipeline():
    """Example: Complete pipeline from PGN to JSON."""
    print("=" * 60)
    print("Example 6: PGN → Validation → JSON Pipeline")
    print("=" * 60)

    # Step 1: Parse PGN
    pgn = """
[Event "Speed Chess"]
[Site "chess.com"]
[Date "2024.01.13"]
[White "FastPlayer"]
[Black "QuickThinker"]
[Result "1-0"]
[Termination "Time forfeit"]

1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 1-0
"""

    game = Game.from_pgn(pgn)
    print("✓ Parsed PGN successfully")

    # Step 2: Validate (automatically done)
    print(f"✓ Validated {len(game.moves)} moves")

    # Step 3: Add custom analysis
    game.moves[0].comments.append(
        Comment(text="Sicilian Defense", source="opening_classifier")
    )
    print("✓ Added custom annotation")

    # Step 4: Export to JSON
    json_output = game.model_dump_json(by_alias=True)
    print(f"✓ Exported to JSON ({len(json_output)} characters)")

    # Step 5: Re-parse to verify
    game_reparsed = Game.model_validate_json(json_output)
    print(
        f"✓ Re-parsed successfully: {game_reparsed.white.name} vs {game_reparsed.black.name}"
    )
    print()


if __name__ == "__main__":
    print("\n")
    print("chess-schema Example Usage")
    print("=" * 60)
    print()

    try:
        example_from_pgn()
        example_manual_construction()
        example_with_variations()
        example_json_serialization()
        example_validation()
        example_pgn_to_json_pipeline()

        print("=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60)
    except ImportError as e:
        if "python-chess" in str(e):
            print("\n⚠️  Some examples require python-chess library")
            print("Install with: pip install python-chess\n")
        else:
            raise
