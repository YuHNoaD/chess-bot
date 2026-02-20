"""
Minimal auto_play test
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.evaluation import Evaluator
from src.type_defs.chess_types import Color

# Create position and evaluator (same as auto_play.py)
pos = Position()
evaluator = Evaluator()

print("1. Initial turn:", pos.turn)

# Print starting position (same as auto_play.py)
print("Starting position...")
print(f"Position score: {evaluator.evaluate(pos):.1f}")

print("2. After evaluation:", pos.turn)

# Loop (same as auto_play.py)
for move_num in range(1, 4):
    print(f"3.{move_num}. Move {move_num}:", pos.turn)

print("4. After loop:", pos.turn)