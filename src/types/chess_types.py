"""
Core type definitions for chess
Similar to Stockfish's type.h
"""

from enum import IntEnum
from typing import Optional, Tuple


class Color(IntEnum):
    """Chess colors"""
    WHITE = 0
    BLACK = 1

    def opposite(self) -> "Color":
        """Get opposite color"""
        return Color.BLACK if self == Color.WHITE else Color.WHITE


class PieceType(IntEnum):
    """Chess piece types"""
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def __str__(self) -> str:
        return ["P", "N", "B", "R", "Q", "K"][self]


class Piece:
    """Chess piece with color and type"""

    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.piece_type = piece_type

    def __eq__(self, other) -> bool:
        if not isinstance(other, Piece):
            return False
        return self.color == other.color and self.piece_type == other.piece_type

    def __hash__(self) -> int:
        return hash((self.color, self.piece_type))

    def __repr__(self) -> str:
        color_str = "W" if self.color == Color.WHITE else "B"
        return f"{color_str}{self.piece_type}"

    def is_slider(self) -> bool:
        """Check if piece is a slider (bishop, rook, queen)"""
        return self.piece_type in [PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]

    def is_stepper(self) -> bool:
        """Check if piece is a stepper (knight, king)"""
        return self.piece_type in [PieceType.KNIGHT, PieceType.KING]


class Square(IntEnum):
    """Chess squares (a1=0, h8=63)"""
    A1 = 0
    B1 = 1
    C1 = 2
    D1 = 3
    E1 = 4
    F1 = 5
    G1 = 6
    H1 = 7
    A2 = 8
    B2 = 9
    C2 = 10
    D2 = 11
    E2 = 12
    F2 = 13
    G2 = 14
    H2 = 15
    A3 = 16
    B3 = 17
    C3 = 18
    D3 = 19
    E3 = 20
    F3 = 21
    G3 = 22
    H3 = 23
    A4 = 24
    B4 = 25
    C4 = 26
    D4 = 27
    E4 = 28
    F4 = 29
    G4 = 30
    H4 = 31
    A5 = 32
    B5 = 33
    C5 = 34
    D5 = 35
    E5 = 36
    F5 = 37
    G5 = 38
    H5 = 39
    A6 = 40
    B6 = 41
    C6 = 42
    D6 = 43
    E6 = 44
    F6 = 45
    G6 = 46
    H6 = 47
    A7 = 48
    B7 = 49
    C7 = 50
    D7 = 51
    E7 = 52
    F7 = 53
    G7 = 54
    H7 = 55
    A8 = 56
    B8 = 57
    C8 = 58
    D8 = 59
    E8 = 60
    F8 = 61
    G8 = 62
    H8 = 63

    @classmethod
    def from_string(cls, s: str) -> "Square":
        """Create square from string (e.g., 'e4')"""
        file = ord(s[0]) - ord('a')
        rank = int(s[1]) - 1
        return cls(rank * 8 + file)

    def __str__(self) -> str:
        file = chr(ord('a') + (self.value % 8))
        rank = (self.value // 8) + 1
        return f"{file}{rank}"

    def file(self) -> int:
        """Get file (0-7)"""
        return self.value % 8

    def rank(self) -> int:
        """Get rank (0-7)"""
        return self.value // 8

    def is_light_square(self) -> bool:
        """Check if square is light-colored"""
        return (self.file() + self.rank()) % 2 == 1

    def is_dark_square(self) -> bool:
        """Check if square is dark-colored"""
        return (self.file() + self.rank()) % 2 == 0


class MoveFlag(IntEnum):
    """Move flags"""
    NORMAL = 0
    DOUBLE_PAWN = 1
    EN_PASSANT = 2
    CASTLE_KING = 3
    CASTLE_QUEEN = 4
    PROMOTION = 5


class Move:
    """Chess move"""

    def __init__(
        self,
        from_sq: Square,
        to_sq: Square,
        flag: MoveFlag = MoveFlag.NORMAL,
        promotion: Optional[PieceType] = None
    ):
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.flag = flag
        self.promotion = promotion

    def __eq__(self, other) -> bool:
        if not isinstance(other, Move):
            return False
        return (
            self.from_sq == other.from_sq and
            self.to_sq == other.to_sq and
            self.flag == other.flag and
            self.promotion == other.promotion
        )

    def __hash__(self) -> int:
        return hash((self.from_sq, self.to_sq, self.flag, self.promotion))

    def __repr__(self) -> str:
        return f"Move({self.from_sq}{self.to_sq}, flag={self.flag}, promo={self.promotion})"

    def __str__(self) -> str:
        move_str = f"{self.from_sq}{self.to_sq}"
        if self.promotion:
            move_str += str(self.promotion).lower()
        return move_str

    def is_capture(self) -> bool:
        """Check if move is a capture"""
        return self.flag in [MoveFlag.EN_PASSANT]

    def is_castle(self) -> bool:
        """Check if move is a castle"""
        return self.flag in [MoveFlag.CASTLE_KING, MoveFlag.CASTLE_QUEEN]

    def is_promotion(self) -> bool:
        """Check if move is a promotion"""
        return self.flag == MoveFlag.PROMOTION

    def is_double_pawn(self) -> bool:
        """Check if move is a double pawn push"""
        return self.flag == MoveFlag.DOUBLE_PAWN

    def is_en_passant(self) -> bool:
        """Check if move is en passant"""
        return self.flag == MoveFlag.EN_PASSANT


# Piece values (in centipawns)
PIECE_VALUES = {
    PieceType.PAWN: 100,
    PieceType.KNIGHT: 320,
    PieceType.BISHOP: 330,
    PieceType.ROOK: 500,
    PieceType.QUEEN: 900,
    PieceType.KING: 20000,
}


# Piece-square tables for evaluation
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MIDDLE_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

KING_END_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

PIECE_SQUARE_TABLES = {
    PieceType.PAWN: PAWN_TABLE,
    PieceType.KNIGHT: KNIGHT_TABLE,
    PieceType.BISHOP: BISHOP_TABLE,
    PieceType.ROOK: ROOK_TABLE,
    PieceType.QUEEN: QUEEN_TABLE,
    PieceType.KING: KING_MIDDLE_TABLE,
}