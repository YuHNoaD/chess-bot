"""
Position/Board representation
Similar to Stockfish's position.{h,cpp}
"""

from typing import List, Optional, Dict, Tuple
import copy

from ..types import Color, PieceType, Piece, Square, Move, MoveFlag


class Position:
    """Chess position representation"""

    def __init__(self, fen: Optional[str] = None):
        """Initialize position from FEN string or starting position"""
        self.board: List[Optional[Piece]] = [None] * 64
        self.turn: Color = Color.WHITE
        self.castling: Dict[Color, Dict[str, bool]] = {
            Color.WHITE: {"king": True, "queen": True},
            Color.BLACK: {"king": True, "queen": True},
        }
        self.en_passant: Optional[Square] = None
        self.halfmove_clock: int = 0
        self.fullmove_number: int = 1

        if fen:
            self.load_fen(fen)
        else:
            self.reset()

    def reset(self) -> None:
        """Reset to starting position"""
        # Clear board
        self.board = [None] * 64

        # Place pieces
        # Black pieces
        self.board[Square.A8] = Piece(Color.BLACK, PieceType.ROOK)
        self.board[Square.B8] = Piece(Color.BLACK, PieceType.KNIGHT)
        self.board[Square.C8] = Piece(Color.BLACK, PieceType.BISHOP)
        self.board[Square.D8] = Piece(Color.BLACK, PieceType.QUEEN)
        self.board[Square.E8] = Piece(Color.BLACK, PieceType.KING)
        self.board[Square.F8] = Piece(Color.BLACK, PieceType.BISHOP)
        self.board[Square.G8] = Piece(Color.BLACK, PieceType.KNIGHT)
        self.board[Square.H8] = Piece(Color.BLACK, PieceType.ROOK)

        for file in range(8):
            self.board[Square.A7 + file] = Piece(Color.BLACK, PieceType.PAWN)

        # White pieces
        for file in range(8):
            self.board[Square.A2 + file] = Piece(Color.WHITE, PieceType.PAWN)

        self.board[Square.A1] = Piece(Color.WHITE, PieceType.ROOK)
        self.board[Square.B1] = Piece(Color.WHITE, PieceType.KNIGHT)
        self.board[Square.C1] = Piece(Color.WHITE, PieceType.BISHOP)
        self.board[Square.D1] = Piece(Color.WHITE, PieceType.QUEEN)
        self.board[Square.E1] = Piece(Color.WHITE, PieceType.KING)
        self.board[Square.F1] = Piece(Color.WHITE, PieceType.BISHOP)
        self.board[Square.G1] = Piece(Color.WHITE, PieceType.KNIGHT)
        self.board[Square.H1] = Piece(Color.WHITE, PieceType.ROOK)

        # Reset state
        self.turn = Color.WHITE
        self.castling = {
            Color.WHITE: {"king": True, "queen": True},
            Color.BLACK: {"king": True, "queen": True},
        }
        self.en_passant = None
        self.halfmove_clock = 0
        self.fullmove_number = 1

    def load_fen(self, fen: str) -> None:
        """Load position from FEN string"""
        parts = fen.split()

        # Parse board
        board_part = parts[0]
        rank = 7
        file = 0

        for c in board_part:
            if c == '/':
                rank -= 1
                file = 0
            elif c.isdigit():
                file += int(c)
            else:
                # Determine color
                color = Color.WHITE if c.isupper() else Color.BLACK

                # Determine piece type
                piece_char = c.lower()
                piece_type_map = {
                    'p': PieceType.PAWN,
                    'n': PieceType.KNIGHT,
                    'b': PieceType.BISHOP,
                    'r': PieceType.ROOK,
                    'q': PieceType.QUEEN,
                    'k': PieceType.KING,
                }
                piece_type = piece_type_map[piece_char]

                # Place piece
                square = rank * 8 + file
                self.board[square] = Piece(color, piece_type)
                file += 1

        # Parse turn
        if len(parts) > 1:
            self.turn = Color.WHITE if parts[1] == 'w' else Color.BLACK

        # Parse castling
        if len(parts) > 2:
            castling_part = parts[2]
            self.castling = {
                Color.WHITE: {"king": False, "queen": False},
                Color.BLACK: {"king": False, "queen": False},
            }

            if 'K' in castling_part:
                self.castling[Color.WHITE]["king"] = True
            if 'Q' in castling_part:
                self.castling[Color.WHITE]["queen"] = True
            if 'k' in castling_part:
                self.castling[Color.BLACK]["king"] = True
            if 'q' in castling_part:
                self.castling[Color.BLACK]["queen"] = True

        # Parse en passant
        if len(parts) > 3 and parts[3] != '-':
            self.en_passant = Square.from_string(parts[3])
        else:
            self.en_passant = None

        # Parse clocks
        if len(parts) > 4:
            self.halfmove_clock = int(parts[4])
        if len(parts) > 5:
            self.fullmove_number = int(parts[5])

    def to_fen(self) -> str:
        """Convert position to FEN string"""
        fen_parts = []

        # Board
        board_str = ""
        for rank in range(7, -1, -1):
            empty_count = 0
            for file in range(8):
                square = rank * 8 + file
                piece = self.board[square]

                if piece is None:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        board_str += str(empty_count)
                        empty_count = 0

                    # Piece character
                    piece_char = str(piece.piece_type)
                    if piece.color == Color.BLACK:
                        piece_char = piece_char.lower()
                    else:
                        piece_char = piece_char.upper()

                    board_str += piece_char

            if empty_count > 0:
                board_str += str(empty_count)

            if rank > 0:
                board_str += '/'

        fen_parts.append(board_str)

        # Turn
        fen_parts.append('w' if self.turn == Color.WHITE else 'b')

        # Castling
        castling_str = ""
        if self.castling[Color.WHITE]["king"]:
            castling_str += 'K'
        if self.castling[Color.WHITE]["queen"]:
            castling_str += 'Q'
        if self.castling[Color.BLACK]["king"]:
            castling_str += 'k'
        if self.castling[Color.BLACK]["queen"]:
            castling_str += 'q'

        if not castling_str:
            castling_str = '-'

        fen_parts.append(castling_str)

        # En passant
        if self.en_passant:
            fen_parts.append(str(self.en_passant))
        else:
            fen_parts.append('-')

        # Clocks
        fen_parts.append(str(self.halfmove_clock))
        fen_parts.append(str(self.fullmove_number))

        return ' '.join(fen_parts)

    def get_piece(self, square: Square) -> Optional[Piece]:
        """Get piece at square"""
        return self.board[square.value]

    def set_piece(self, square: Square, piece: Optional[Piece]) -> None:
        """Set piece at square"""
        self.board[square.value] = piece

    def make_move(self, move: Move) -> None:
        """Make a move on the board"""
        from_sq = move.from_sq
        to_sq = move.to_sq
        piece = self.get_piece(from_sq)

        if piece is None:
            raise ValueError(f"No piece at {from_sq}")

        # Move piece
        self.set_piece(to_sq, piece)
        self.set_piece(from_sq, None)

        # Handle special moves
        if move.is_castle():
            self._handle_castle(move)
        elif move.is_en_passant():
            self._handle_en_passant(move)
        elif move.is_promotion():
            self.set_piece(to_sq, Piece(piece.color, move.promotion))

        # Update castling rights
        self._update_castling_rights(move)

        # Update en passant
        if move.is_double_pawn():
            rank = (from_sq.rank() + to_sq.rank()) // 2
            self.en_passant = Square(to_sq.file() * 8 + rank)
        else:
            self.en_passant = None

        # Update clocks
        if piece.piece_type == PieceType.PAWN or self.get_piece(to_sq) is not None:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.turn == Color.BLACK:
            self.fullmove_number += 1

        # Switch turn
        self.turn = self.turn.opposite()

    def _handle_castle(self, move: Move) -> None:
        """Handle castling"""
        if move.flag == MoveFlag.CASTLE_KING:
            # Kingside castle
            rank = move.from_sq.rank()
            rook_from = Square(rank * 8 + 7)  # h-file
            rook_to = Square(rank * 8 + 5)    # f-file
            rook = self.get_piece(rook_from)
            self.set_piece(rook_to, rook)
            self.set_piece(rook_from, None)
        elif move.flag == MoveFlag.CASTLE_QUEEN:
            # Queenside castle
            rank = move.from_sq.rank()
            rook_from = Square(rank * 8 + 0)  # a-file
            rook_to = Square(rank * 8 + 3)    # d-file
            rook = self.get_piece(rook_from)
            self.set_piece(rook_to, rook)
            self.set_piece(rook_from, None)

    def _handle_en_passant(self, move: Move) -> None:
        """Handle en passant capture"""
        capture_sq = Square(move.to_sq.rank() * 8 + move.from_sq.file())
        self.set_piece(capture_sq, None)

    def _update_castling_rights(self, move: Move) -> None:
        """Update castling rights after move"""
        from_sq = move.from_sq
        to_sq = move.to_sq
        piece = self.get_piece(to_sq)

        # King move
        if piece and piece.piece_type == PieceType.KING:
            self.castling[piece.color]["king"] = False
            self.castling[piece.color]["queen"] = False

        # Rook moves
        if from_sq == Square.A1:
            self.castling[Color.WHITE]["queen"] = False
        elif from_sq == Square.H1:
            self.castling[Color.WHITE]["king"] = False
        elif from_sq == Square.A8:
            self.castling[Color.BLACK]["queen"] = False
        elif from_sq == Square.H8:
            self.castling[Color.BLACK]["king"] = False

        # Rook capture
        if to_sq == Square.A1:
            self.castling[Color.WHITE]["queen"] = False
        elif to_sq == Square.H1:
            self.castling[Color.WHITE]["king"] = False
        elif to_sq == Square.A8:
            self.castling[Color.BLACK]["queen"] = False
        elif to_sq == Square.H8:
            self.castling[Color.BLACK]["king"] = False

    def copy(self) -> "Position":
        """Create a copy of the position"""
        new_pos = Position()
        new_pos.board = self.board.copy()
        new_pos.turn = self.turn
        new_pos.castling = copy.deepcopy(self.castling)
        new_pos.en_passant = self.en_passant
        new_pos.halfmove_clock = self.halfmove_clock
        new_pos.fullmove_number = self.fullmove_number
        return new_pos

    def __str__(self) -> str:
        """String representation of position"""
        lines = []
        lines.append("  a b c d e f g h")

        for rank in range(7, -1, -1):
            line = f"{rank + 1} "
            for file in range(8):
                square = rank * 8 + file
                piece = self.board[square]

                if piece is None:
                    # Light or dark square
                    sq = Square(square)
                    if sq.is_light_square():
                        line += ". "
                    else:
                        line += "# "
                else:
                    # Piece character
                    piece_char = str(piece.piece_type)
                    if piece.color == Color.BLACK:
                        piece_char = piece_char.lower()
                    else:
                        piece_char = piece_char.upper()

                    line += piece_char + " "

            lines.append(line)

        lines.append(f"  a b c d e f g h")
        lines.append(f"FEN: {self.to_fen()}")

        return '\n'.join(lines)