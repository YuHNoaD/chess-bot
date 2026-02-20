"""
Position evaluation
Similar to Stockfish's evaluation.{h,cpp}
"""

from typing import Dict

from ..types.chess_types import Color, PieceType, Piece, Square, PIECE_VALUES, PIECE_SQUARE_TABLES
from ..position import Position
import config


class Evaluator:
    """Evaluate chess positions"""

    def __init__(self):
        self.material_weight = config.MATERIAL_WEIGHT
        self.position_weight = config.POSITION_WEIGHT
        self.mobility_weight = config.MOBILITY_WEIGHT
        self.king_safety_weight = config.KING_SAFETY_WEIGHT
        self.pawn_structure_weight = config.PAWN_STRUCTURE_WEIGHT

    def evaluate(self, position: Position) -> int:
        """
        Evaluate position from white's perspective
        Positive = white is better
        Negative = black is better
        """
        score = 0

        # Material evaluation
        score += self.material_weight * self.evaluate_material(position)

        # Position evaluation
        score += self.position_weight * self.evaluate_position(position)

        # Mobility evaluation
        score += self.mobility_weight * self.evaluate_mobility(position)

        # King safety evaluation
        score += self.king_safety_weight * self.evaluate_king_safety(position)

        # Pawn structure evaluation
        score += self.pawn_structure_weight * self.evaluate_pawn_structure(position)

        return score

    def evaluate_material(self, position: Position) -> int:
        """Evaluate material balance"""
        score = 0

        for square in Square:
            piece = position.get_piece(square)
            if piece is None:
                continue

            piece_value = PIECE_VALUES[piece.piece_type]

            if piece.color == Color.WHITE:
                score += piece_value
            else:
                score -= piece_value

        return score

    def evaluate_position(self, position: Position) -> int:
        """Evaluate piece placement using piece-square tables"""
        score = 0

        for square in Square:
            piece = position.get_piece(square)
            if piece is None:
                continue

            # Get piece-square table
            table = PIECE_SQUARE_TABLES.get(piece.piece_type, [0] * 64)

            # Get value from table
            if piece.color == Color.WHITE:
                # White: use table as-is
                value = table[square.value]
                score += value
            else:
                # Black: mirror the table
                mirrored_value = table[63 - square.value]
                score -= mirrored_value

        return score

    def evaluate_mobility(self, position: Position) -> int:
        """Evaluate mobility (number of legal moves)"""
        from ..movegen import MoveGenerator

        score = 0

        # White mobility
        position.turn = Color.WHITE
        movegen_white = MoveGenerator(position)
        white_moves = len(movegen_white.generate_legal_moves())
        score += white_moves

        # Black mobility
        position.turn = Color.BLACK
        movegen_black = MoveGenerator(position)
        black_moves = len(movegen_black.generate_legal_moves())
        score -= black_moves

        return score

    def evaluate_king_safety(self, position: Position) -> int:
        """Evaluate king safety"""
        score = 0

        # Find kings
        white_king_sq = None
        black_king_sq = None

        for square in Square:
            piece = position.get_piece(square)
            if piece and piece.piece_type == PieceType.KING:
                if piece.color == Color.WHITE:
                    white_king_sq = square
                else:
                    black_king_sq = square

        # Evaluate white king safety
        if white_king_sq:
            score += self.evaluate_single_king_safety(
                position, white_king_sq, Color.WHITE
            )

        # Evaluate black king safety
        if black_king_sq:
            score -= self.evaluate_single_king_safety(
                position, black_king_sq, Color.BLACK
            )

        return score

    def evaluate_single_king_safety(
        self, position: Position, king_sq: Square, color: Color
    ) -> int:
        """Evaluate safety of a single king"""
        safety = 0

        # Penalty for king in center
        center_squares = [
            Square.D3, Square.D4, Square.D5, Square.D6,
            Square.E3, Square.E4, Square.E5, Square.E6,
        ]
        if king_sq in center_squares:
            safety -= 30

        # Bonus for king on back rank
        if color == Color.WHITE and king_sq.rank() == 0:
            safety += 20
        elif color == Color.BLACK and king_sq.rank() == 7:
            safety += 20

        # Penalty for exposed king
        if self.is_king_exposed(position, king_sq, color):
            safety -= 50

        return safety

    def is_king_exposed(
        self, position: Position, king_sq: Square, color: Color
    ) -> bool:
        """Check if king is exposed (no pawn protection)"""
        direction = 1 if color == Color.WHITE else -1

        # Check squares in front of king
        for dc in [-1, 0, 1]:
            new_file = king_sq.file() + dc
            if 0 <= new_file < 8:
                pawn_sq = Square(
                    king_sq.value + direction * 8 + dc
                )
                pawn = position.get_piece(pawn_sq)

                if pawn and pawn.piece_type == PieceType.PAWN and pawn.color == color:
                    return False

        return True

    def evaluate_pawn_structure(self, position: Position) -> int:
        """Evaluate pawn structure"""
        score = 0

        # Find pawns
        white_pawns = []
        black_pawns = []

        for square in Square:
            piece = position.get_piece(square)
            if piece and piece.piece_type == PieceType.PAWN:
                if piece.color == Color.WHITE:
                    white_pawns.append(square)
                else:
                    black_pawns.append(square)

        # Evaluate white pawn structure
        score += self.evaluate_pawn_structure_color(
            position, white_pawns, Color.WHITE
        )

        # Evaluate black pawn structure
        score -= self.evaluate_pawn_structure_color(
            position, black_pawns, Color.BLACK
        )

        return score

    def evaluate_pawn_structure_color(
        self, position: Position, pawns: list, color: Color
    ) -> int:
        """Evaluate pawn structure for one color"""
        structure_score = 0

        # Check for doubled pawns
        file_counts = {}
        for pawn in pawns:
            file = pawn.file()
            file_counts[file] = file_counts.get(file, 0) + 1

        for count in file_counts.values():
            if count > 1:
                structure_score -= 15 * (count - 1)

        # Check for isolated pawns
        for pawn in pawns:
            file = pawn.file()
            has_neighbor = False

            # Check adjacent files
            for adj_file in [file - 1, file + 1]:
                if 0 <= adj_file < 8:
                    for other_pawn in pawns:
                        if other_pawn.file() == adj_file:
                            has_neighbor = True
                            break

            if not has_neighbor:
                structure_score -= 20

        # Check for passed pawns
        for pawn in pawns:
            if self.is_passed_pawn(position, pawn, color):
                structure_score += 20

        # Check for backward pawns
        for pawn in pawns:
            if self.is_backward_pawn(position, pawn, color):
                structure_score -= 10

        return structure_score

    def is_passed_pawn(
        self, position: Position, pawn_sq: Square, color: Color
    ) -> bool:
        """Check if pawn is passed"""
        direction = 1 if color == Color.WHITE else -1

        # Check all squares ahead
        for rank in range(pawn_sq.rank() + direction, 8 if color == Color.WHITE else -1, direction):
            for file in range(max(0, pawn_sq.file() - 1), min(8, pawn_sq.file() + 2)):
                check_sq = Square(rank * 8 + file)
                piece = position.get_piece(check_sq)

                if piece and piece.piece_type == PieceType.PAWN and piece.color != color:
                    return False

        return True

    def is_backward_pawn(
        self, position: Position, pawn_sq: Square, color: Color
    ) -> bool:
        """Check if pawn is backward"""
        direction = 1 if color == Color.WHITE else -1

        # Check if pawn has no pawn protection
        has_support = False

        for file in [pawn_sq.file() - 1, pawn_sq.file() + 1]:
            if 0 <= file < 8:
                support_sq = Square(
                    pawn_sq.value - direction * 8 + (file - pawn_sq.file())
                )
                support_piece = position.get_piece(support_sq)

                if (support_piece and
                    support_piece.piece_type == PieceType.PAWN and
                    support_piece.color == color):
                    has_support = True
                    break

        if has_support:
            return False

        # Check if pawn can advance safely
        advance_sq = Square(pawn_sq.value + direction * 8)
        if 0 <= advance_sq.value < 64:
            advance_piece = position.get_piece(advance_sq)

            if advance_piece is None:
                # Check if controlled by opponent pawn
                for file in [advance_sq.file() - 1, advance_sq.file() + 1]:
                    if 0 <= file < 8:
                        control_sq = Square(
                            advance_sq.value - direction * 8 + (file - advance_sq.file())
                        )
                        control_piece = position.get_piece(control_sq)

                        if (control_piece and
                            control_piece.piece_type == PieceType.PAWN and
                            control_piece.color != color):
                            return True

        return False