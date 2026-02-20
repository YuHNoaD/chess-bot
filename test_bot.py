"""
Test script for ChessBot
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.movegen import MoveGenerator
from src.search import Search
from src.evaluation import Evaluator
from src.type_defs.chess_types import Square, Color, Move, MoveFlag

def test_basic():
    """Test basic functionality"""
    print("=" * 60)
    print("Testing ChessBot - Basic Functionality")
    print("=" * 60)

    # Test 1: Create position
    print("\n[Test 1] Creating starting position...")
    pos = Position()
    print(f"[OK] Position created")
    print(f"FEN: {pos.to_fen()[:50]}...")

    # Test 2: Generate moves
    print("\n[Test 2] Generating legal moves...")
    movegen = MoveGenerator(pos)
    moves = movegen.generate_legal_moves()
    print(f"[OK] Generated {len(moves)} legal moves")

    # Print first 5 moves
    print(f"First 5 moves: {[str(m) for m in moves[:5]]}")

    # Test 3: Evaluate position
    print("\n[Test 3] Evaluating position...")
    evaluator = Evaluator()
    score = evaluator.evaluate(pos)
    print(f"[OK] Position score: {score}")
    print(f"   (Positive = white advantage, Negative = black advantage)")

    # Test 4: Make a move
    print("\n[Test 4] Making move e2e4...")
    move = Move(Square.E2, Square.E4)
    pos.make_move(move)
    print(f"[OK] Move made")
    print(f"FEN after move: {pos.to_fen()[:50]}...")

    # Test 5: Evaluate after move
    print("\n[Test 5] Evaluating after e2e4...")
    score = evaluator.evaluate(pos)
    print(f"[OK] Position score: {score}")

    # Test 6: Find best move
    print("\n[Test 6] Finding best move (depth 3)...")
    pos = Position()  # Reset to start
    search = Search(pos)
    best_move = search.find_best_move(depth=3, time_limit=2.0)
    if best_move:
        print(f"[OK] Best move found: {best_move}")
        print(f"   Nodes searched: {search.get_nodes_searched()}")
    else:
        print("[ERROR] No best move found")

    # Test 7: Test with a tactical position
    print("\n[Test 7] Testing tactical position (Scholar's Mate)...")
    # Scholar's Mate position
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 3"
    pos = Position(fen)
    print(f"FEN: {fen[:50]}...")
    
    search = Search(pos)
    best_move = search.find_best_move(depth=3, time_limit=2.0)
    if best_move:
        print(f"[OK] Best move found: {best_move}")
        print(f"   (Expected: Qxf7# for mate in 1)")
    else:
        print("[ERROR] No best move found")

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_basic()