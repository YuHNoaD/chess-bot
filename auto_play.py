"""
Auto play demo - White vs Black (Bot plays both sides)
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.search import Search
from src.evaluation import Evaluator
from src.movegen import MoveGenerator
from src.type_defs.chess_types import Square, Color

def print_board(pos):
    """Print the chess board"""
    print("\n  a b c d e f g h")

    for rank in range(7, -1, -1):
        line = f"{rank + 1} "
        for file in range(8):
            square = rank * 8 + file
            piece = pos.get_piece(Square(square))

            if piece is None:
                line += ". "
            else:
                # Piece character
                piece_chars = {
                    (Color.WHITE, 0): 'P',
                    (Color.WHITE, 1): 'N',
                    (Color.WHITE, 2): 'B',
                    (Color.WHITE, 3): 'R',
                    (Color.WHITE, 4): 'Q',
                    (Color.WHITE, 5): 'K',
                    (Color.BLACK, 0): 'p',
                    (Color.BLACK, 1): 'n',
                    (Color.BLACK, 2): 'b',
                    (Color.BLACK, 3): 'r',
                    (Color.BLACK, 4): 'q',
                    (Color.BLACK, 5): 'k',
                }
                line += piece_chars[(piece.color, piece.piece_type)] + " "

        print(line)

    print("  a b c d e f g h")

def auto_play():
    """Auto play a few moves"""
    print("=" * 60)
    print("CHESS BOT - AUTO PLAY DEMO")
    print("Bot plays both White and Black")
    print("=" * 60)
    print()

    pos = Position()
    evaluator = Evaluator()

    # Play 10 moves (5 each)
    moves_to_play = 10

    print("Starting position:")
    print_board(pos)
    print(f"Position score: {evaluator.evaluate(pos):.1f} (positive = White advantage)")
    print()

    for move_num in range(1, moves_to_play + 1):
        # Check turn BEFORE making move
        turn_str = "White" if pos.turn == Color.WHITE else "Black"
        print(f"Move {move_num} - {turn_str}'s turn")
        print("-" * 60)

        # Find best move
        print("Thinking...")
        search = Search(pos)
        best_move = search.find_best_move(depth=3, time_limit=2.0)

        if best_move:
            print(f"Best move: {best_move}")
            print(f"Nodes searched: {search.get_nodes_searched()}")

            # Make move
            pos.make_move(best_move)

            # Print board
            print_board(pos)

            # Evaluate
            score = evaluator.evaluate(pos)
            print(f"Position score: {score:.1f}")

            # Check if game over
            movegen = MoveGenerator(pos)
            legal_moves = movegen.generate_legal_moves()

            if not legal_moves:
                if movegen.is_in_check(pos.turn):
                    winner = "Black" if pos.turn == Color.WHITE else "White"
                    print(f"\nCHECKMATE! {winner} wins!")
                else:
                    print("\nSTALEMATE! Game is a draw.")
                break
        else:
            print("No legal moves!")
            break

        print()

    print("=" * 60)
    print("GAME OVER")
    print("=" * 60)

if __name__ == "__main__":
    auto_play()