"""
Debug script for move generation
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.movegen import MoveGenerator
from src.type_defs.chess_types import Square

# Test move generation
print("Testing move generation...")
pos = Position()
movegen = MoveGenerator(pos)

moves = movegen.generate_legal_moves()
print(f"Total legal moves: {len(moves)}")

# Check for e2e4
e2e4_move = None
for move in moves:
    if str(move.from_sq) == "e2" and str(move.to_sq) == "e4":
        e2e4_move = move
        break

if e2e4_move:
    print(f"\n[OK] Found e2e4 move: {e2e4_move}")
    print(f"  from_sq: {e2e4_move.from_sq} (value: {e2e4_move.from_sq.value})")
    print(f"  to_sq: {e2e4_move.to_sq} (value: {e2e4_move.to_sq.value})")
    print(f"  flag: {e2e4_move.flag}")
else:
    print(f"\n[ERROR] e2e4 move not found!")

# Print first 10 moves
print(f"\nFirst 10 moves:")
for i, move in enumerate(moves[:10]):
    print(f"  {i+1}. {move.from_sq}{move.to_sq}")