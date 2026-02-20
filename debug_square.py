"""
Debug script for Square.from_string
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.type_defs.chess_types import Square

# Test Square.from_string
print("Testing Square.from_string()...")
print(f"Square.from_string('e2') = {Square.from_string('e2')}")
print(f"Square.E2 = {Square.E2}")
print(f"str(Square.E2) = {str(Square.E2)}")
print(f"Square.from_string('e2') == Square.E2: {Square.from_string('e2') == Square.E2}")

print(f"\nSquare.from_string('e4') = {Square.from_string('e4')}")
print(f"Square.E4 = {Square.E4}")
print(f"str(Square.E4) = {str(Square.E4)}")
print(f"Square.from_string('e4') == Square.E4: {Square.from_string('e4') == Square.E4}")