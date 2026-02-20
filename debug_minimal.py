"""
Minimal turn test
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.type_defs.chess_types import Color

# Create position
pos = Position()

print("1. Initial turn:", pos.turn)

# Just a simple print
print("2. After print:", pos.turn)

# Loop
for i in range(3):
    print(f"3.{i}. Loop iteration {i+1}:", pos.turn)

print("4. After loop:", pos.turn)