"""
Move generation
Similar to Stockfish's movegen.{h,cpp}
"""

from typing import List, Set, Tuple
import itertools

from ..types import Color, PieceType, Piece, Square, Move, MoveFlag
from ..position import Position


class MoveGenerator:
    """Generate legal moves for a position"""

    def __init__(self, position: Position):
        self.position = position

    def generate_legal_moves(self) -> List[Move]:
        """Generate all legal moves for current position"""
        moves = self.generate_pseudo_legal_moves()
        legal_moves = []

        for move in moves:
            # Make move on copy of position
            new_pos = self.position.copy()
            new_pos.make_move(move)

            # Check if move leaves king in check
            if not self.is_in_check(new_pos, self.position.turn):
                legal_moves.append(move)

        return legal_moves

    def generate_pseudo_legal_moves(self) -> List[Move]:
        """Generate pseudo-legal moves (may leave king in check)"""
        moves = []
        turn = self.position.turn

        # Generate moves for each piece
        for square in Square:
            piece = self.position.get_piece(square)
            if piece is None or piece.color != turn:
                continue

            piece_moves = self.generate_piece_moves(square, piece)
            moves.extend(piece_moves)

        return moves

    def generate_piece_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate moves for a specific piece"""
        moves = []

        if piece.piece_type == PieceType.PAWN:
            moves.extend(self.generate_pawn_moves(square, piece))
        elif piece.piece_type == PieceType.KNIGHT:
            moves.extend(self.generate_knight_moves(square, piece))
        elif piece.piece_type == PieceType.BISHOP:
            moves.extend(self.generate_bishop_moves(square, piece))
        elif piece.piece_type == PieceType.ROOK:
            moves.extend(self.generate_rook_moves(square, piece))
        elif piece.piece_type == PieceType.QUEEN:
            moves.extend(self.generate_queen_moves(square, piece))
        elif piece.piece_type == PieceType.KING:
            moves.extend(self.generate_king_moves(square, piece))

        return moves

    def generate_pawn_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate pawn moves"""
        moves = []
        direction = 1 if piece.color == Color.WHITE else -1

        # Single push
        forward_sq = Square(square.value + direction * 8)
        if 0 <= forward_sq.value < 64:
            if self.position.get_piece(forward_sq) is None:
                # Check for promotion
                rank = forward_sq.rank()
                if rank == 0 or rank == 7:
                    promotions = [
                        PieceType.QUEEN,
                        PieceType.ROOK,
                        PieceType.BISHOP,
                        PieceType.KNIGHT,
                    ]
                    for promo in promotions:
                        moves.append(Move(square, forward_sq, MoveFlag.PROMOTION, promo))
                else:
                    moves.append(Move(square, forward_sq))

                    # Double push
                    start_rank = 1 if piece.color == Color.WHITE else 6
                    if rank == start_rank:
                        double_sq = Square(forward_sq.value + direction * 8)
                        if self.position.get_piece(double_sq) is None:
                            moves.append(Move(square, double_sq, MoveFlag.DOUBLE_PAWN))

        # Captures
        capture_files = [square.file() - 1, square.file() + 1]
        for file in capture_files:
            if 0 <= file < 8:
                capture_sq = Square(square.value + direction * 8 + (file - square.file()))
                if 0 <= capture_sq.value < 64:
                    capture_piece = self.position.get_piece(capture_sq)
                    if capture_piece and capture_piece.color != piece.color:
                        rank = capture_sq.rank()
                        if rank == 0 or rank == 7:
                            promotions = [
                                PieceType.QUEEN,
                                PieceType.ROOK,
                                PieceType.BISHOP,
                                PieceType.KNIGHT,
                            ]
                            for promo in promotions:
                                moves.append(Move(square, capture_sq, MoveFlag.PROMOTION, promo))
                        else:
                            moves.append(Move(square, capture_sq))

                    # En passant
                    if self.position.en_passant == capture_sq:
                        moves.append(Move(square, capture_sq, MoveFlag.EN_PASSANT))

        return moves

    def generate_knight_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate knight moves"""
        moves = []
        knight_offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1),
        ]

        for dr, dc in knight_offsets:
            new_rank = square.rank() + dr
            new_file = square.file() + dc

            if 0 <= new_rank < 8 and 0 <= new_file < 8:
                target_sq = Square(new_rank * 8 + new_file)
                target_piece = self.position.get_piece(target_sq)

                if target_piece is None or target_piece.color != piece.color:
                    moves.append(Move(square, target_sq))

        return moves

    def generate_bishop_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate bishop moves"""
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_rank = square.rank() + dr * i
                new_file = square.file() + dc * i

                if not (0 <= new_rank < 8 and 0 <= new_file < 8):
                    break

                target_sq = Square(new_rank * 8 + new_file)
                target_piece = self.position.get_piece(target_sq)

                if target_piece is None:
                    moves.append(Move(square, target_sq))
                else:
                    if target_piece.color != piece.color:
                        moves.append(Move(square, target_sq))
                    break

        return moves

    def generate_rook_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate rook moves"""
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_rank = square.rank() + dr * i
                new_file = square.file() + dc * i

                if not (0 <= new_rank < 8 and 0 <= new_file < 8):
                    break

                target_sq = Square(new_rank * 8 + new_file)
                target_piece = self.position.get_piece(target_sq)

                if target_piece is None:
                    moves.append(Move(square, target_sq))
                else:
                    if target_piece.color != piece.color:
                        moves.append(Move(square, target_sq))
                    break

        return moves

    def generate_queen_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate queen moves"""
        moves = []

        # Bishop moves
        moves.extend(self.generate_bishop_moves(square, piece))

        # Rook moves
        moves.extend(self.generate_rook_moves(square, piece))

        return moves

    def generate_king_moves(self, square: Square, piece: Piece) -> List[Move]:
        """Generate king moves"""
        moves = []

        # Normal moves
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                new_rank = square.rank() + dr
                new_file = square.file() + dc

                if 0 <= new_rank < 8 and 0 <= new_file < 8:
                    target_sq = Square(new_rank * 8 + new_file)
                    target_piece = self.position.get_piece(target_sq)

                    if target_piece is None or target_piece.color != piece.color:
                        moves.append(Move(square, target_sq))

        # Castling
        if self.can_castle_king(piece.color):
            moves.append(Move(square, Square(square.value + 2), MoveFlag.CASTLE_KING))

        if self.can_castle_queen(piece.color):
            moves.append(Move(square, Square(square.value - 2), MoveFlag.CASTLE_QUEEN))

        return moves

    def can_castle_king(self, color: Color) -> bool:
        """Check if kingside castling is possible"""
        if not self.position.castling[color]["king"]:
            return False

        if self.is_in_check(self.position, color):
            return False

        # Check squares between king and rook
        rank = 0 if color == Color.WHITE else 7
        king_sq = Square(rank * 8 + 4)

        if self.position.get_piece(Square(rank * 8 + 5)) is not None:
            return False

        if self.position.get_piece(Square(rank * 8 + 6)) is not None:
            return False

        # Check if passing through check
        pass_sq = Square(rank * 8 + 5)
        new_pos = self.position.copy()
        new_pos.set_piece(king_sq, None)
        new_pos.set_piece(pass_sq, Piece(color, PieceType.KING))

        if self.is_in_check(new_pos, color):
            return False

        return True

    def can_castle_queen(self, color: Color) -> bool:
        """Check if queenside castling is possible"""
        if not self.position.castling[color]["queen"]:
            return False

        if self.is_in_check(self.position, color):
            return False

        # Check squares between king and rook
        rank = 0 if color == Color.WHITE else 7
        king_sq = Square(rank * 8 + 4)

        if self.position.get_piece(Square(rank * 8 + 3)) is not None:
            return False

        if self.position.get_piece(Square(rank * 8 + 2)) is not None:
            return False

        if self.position.get_piece(Square(rank * 8 + 1)) is not None:
            return False

        # Check if passing through check
        pass_sq = Square(rank * 8 + 3)
        new_pos = self.position.copy()
        new_pos.set_piece(king_sq, None)
        new_pos.set_piece(pass_sq, Piece(color, PieceType.KING))

        if self.is_in_check(new_pos, color):
            return False

        return True

    def is_in_check(self, position: Position, color: Color) -> bool:
        """Check if color is in check"""
        # Find king
        king_sq = None
        for square in Square:
            piece = position.get_piece(square)
            if piece and piece.piece_type == PieceType.KING and piece.color == color:
                king_sq = square
                break

        if king_sq is None:
            return True

        # Check if any opponent piece attacks the king
        opponent = color.opposite()
        for square in Square:
            piece = position.get_piece(square)
            if piece and piece.color == opponent:
                if self.square_attacked_by(square, king_sq, position):
                    return True

        return False

    def square_attacked_by(self, attacker_sq: Square, target_sq: Square, position: Position) -> bool:
        """Check if attacker_sq attacks target_sq"""
        attacker = position.get_piece(attacker_sq)
        if attacker is None:
            return False

        # Generate pseudo-legal moves for attacker
        temp_gen = MoveGenerator(position)

        if attacker.piece_type == PieceType.PAWN:
            direction = 1 if attacker.color == Color.WHITE else -1
            capture_files = [attacker_sq.file() - 1, attacker_sq.file() + 1]
            for file in capture_files:
                if 0 <= file < 8:
                    capture_sq = Square(
                        attacker_sq.value + direction * 8 + (file - attacker_sq.file())
                    )
                    if capture_sq == target_sq:
                        return True
        elif attacker.piece_type == PieceType.KNIGHT:
            knight_offsets = [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2), (1, 2), (2, -1), (2, 1),
            ]
            for dr, dc in knight_offsets:
                new_rank = attacker_sq.rank() + dr
                new_file = attacker_sq.file() + dc
                if 0 <= new_rank < 8 and 0 <= new_file < 8:
                    check_sq = Square(new_rank * 8 + new_file)
                    if check_sq == target_sq:
                        return True
        elif attacker.piece_type in [PieceType.BISHOP, PieceType.QUEEN]:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_rank = attacker_sq.rank() + dr * i
                    new_file = attacker_sq.file() + dc * i
                    if not (0 <= new_rank < 8 and 0 <= new_file < 8):
                        break
                    check_sq = Square(new_rank * 8 + new_file)
                    if check_sq == target_sq:
                        return True
                    if position.get_piece(check_sq) is not None:
                        break
        elif attacker.piece_type in [PieceType.ROOK, PieceType.QUEEN]:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in directions:
                for i in range(1, 8):
                    new_rank = attacker_sq.rank() + dr * i
                    new_file = attacker_sq.file() + dc * i
                    if not (0 <= new_rank < 8 and 0 <= new_file < 8):
                        break
                    check_sq = Square(new_rank * 8 + new_file)
                    if check_sq == target_sq:
                        return True
                    if position.get_piece(check_sq) is not None:
                        break
        elif attacker.piece_type == PieceType.KING:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_rank = attacker_sq.rank() + dr
                    new_file = attacker_sq.file() + dc
                    if 0 <= new_rank < 8 and 0 <= new_file < 8:
                        check_sq = Square(new_rank * 8 + new_file)
                        if check_sq == target_sq:
                            return True

        return False