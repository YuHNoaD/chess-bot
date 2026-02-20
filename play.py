"""
Simple demo - Play against the bot
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.movegen import MoveGenerator
from src.search import Search
from src.evaluation import Evaluator
from src.type_defs.chess_types import Square, Color, Move

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

def play_game():
    """Play a game against the bot"""
    print("=" * 60)
    print("ChessBot - Play against the bot!")
    print("=" * 60)
    print("\nCommands:")
    print("  - Enter move in algebraic notation (e.g., 'e2e4')")
    print("  - Type 'quit' to exit")
    print("  - Type 'undo' to undo last move")
    print()

    pos = Position()
    movegen = MoveGenerator(pos)
    evaluator = Evaluator()

    print("Starting new game...")
    print_board(pos)

    move_history = []

    while True:
        # Check if game is over
        moves = movegen.generate_legal_moves()
        if not moves:
            if movegen.is_in_check(pos, pos.turn):
                winner = "Black" if pos.turn == Color.WHITE else "White"
                print(f"\nCHECKMATE! {winner} wins!")
            else:
                print("\nSTALEMATE! Game is a draw.")
            break

        # Print whose turn
        turn_str = "White" if pos.turn == Color.WHITE else "Black"
        print(f"\n{turn_str}'s turn")

        # Player's turn (White)
        if pos.turn == Color.WHITE:
            move_str = input("Enter your move: ").strip()

            if move_str.lower() == 'quit':
                print("Game ended.")
                break
            elif move_str.lower() == 'undo':
                if move_history:
                    # Undo last 2 moves (player + bot)
                    pos = move_history[-2]
                    move_history = move_history[:-2]
                    print("Move undone!")
                    print_board(pos)
                else:
                    print("No moves to undo!")
                continue

            # Parse move
            try:
                if len(move_str) < 4:
                    print("Invalid move! Enter move like 'e2e4'")
                    continue

                from_sq = Square.from_string(move_str[0:2])
                to_sq = Square.from_string(move_str[2:4])

                # Check if move is legal
                legal_move = None
                for move in moves:
                    if str(move.from_sq) == move_str[0:2] and str(move.to_sq) == move_str[2:4]:
                        legal_move = move
                        break

                if legal_move:
                    pos.make_move(legal_move)
                    move_history.append(pos.copy())
                    print(f"\nYou played: {move_str}")
                    print_board(pos)

                    # Evaluate
                    score = evaluator.evaluate(pos)
                    print(f"Position score: {score:.1f}")
                else:
                    print("Illegal move! Try again.")

            except Exception as e:
                print(f"Error parsing move: {e}")

        # Bot's turn (Black)
        else:
            print("Bot is thinking...")
            search = Search(pos)
            best_move = search.find_best_move(depth=3, time_limit=2.0)

            if best_move:
                pos.make_move(best_move)
                move_history.append(pos.copy())

                print(f"\nBot played: {best_move}")
                print_board(pos)

                # Evaluate
                score = evaluator.evaluate(pos)
                print(f"Position score: {score:.1f}")
                print(f"Nodes searched: {search.get_nodes_searched()}")
            else:
                print("Bot has no legal moves!")
                break

if __name__ == "__main__":
    play_game()