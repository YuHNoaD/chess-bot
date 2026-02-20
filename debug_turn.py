"""
Debug turn switching
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.type_defs.chess_types import Color, Square

# Create position
pos = Position()

print("Initial turn:", pos.turn, "(0=WHITE, 1=BLACK)")
print()

# Make a simple move (e2e4)
from src.movegen import MoveGenerator
from src.type_defs.chess_types import Move, MoveFlag

movegen = MoveGenerator(pos)
moves = movegen.generate_legal_moves()

if moves:
    move = moves[0]  # First legal move
    print(f"Making move: {move}")
    print(f"Turn before make_move: {pos.turn}")

    pos.make_move(move)

    print(f"Turn after make_move: {pos.turn}")
    print(f"Expected: {Color.BLACK} (1)")
else:
    print("No legal moves!")