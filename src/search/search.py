"""
Search algorithm with alpha-beta pruning
Similar to Stockfish's search.{h,cpp}
"""

import time
from typing import Optional, List, Dict, Tuple
import random

from ..position import Position
from ..types.chess_types import Color, Move, MoveFlag
from ..movegen import MoveGenerator
from ..evaluation import Evaluator
import config


class TranspositionEntry:
    """Transposition table entry"""

    def __init__(
        self,
        hash_key: int,
        score: int,
        depth: int,
        flag: str,
        move: Optional[Move] = None
    ):
        self.hash_key = hash_key
        self.score = score
        self.depth = depth
        self.flag = flag  # 'exact', 'lower', 'upper'
        self.move = move


class Search:
    """Alpha-beta search with transposition table"""

    def __init__(self, position: Position):
        self.position = position
        self.evaluator = Evaluator()
        self.nodes_searched = 0
        self.transposition_table: Dict[int, TranspositionEntry] = {}

    def find_best_move(
        self,
        depth: int = config.SEARCH_DEPTH,
        time_limit: float = config.SEARCH_TIME
    ) -> Optional[Move]:
        """Find best move using iterative deepening"""
        start_time = time.time()
        best_move = None

        # Iterative deepening
        for current_depth in range(1, depth + 1):
            # Check time limit
            if time.time() - start_time > time_limit:
                break

            # Search at current depth
            move, score = self.search(current_depth)

            if move:
                best_move = move

            # Check for checkmate
            if abs(score) > 10000:
                break

        return best_move

    def search(self, depth: int) -> Tuple[Optional[Move], int]:
        """Search at given depth"""
        moves = self._get_ordered_moves()

        if not moves:
            # No moves - checkmate or stalemate
            if self._is_check(self.position.turn):
                return None, -100000 + self.position.fullmove_number
            else:
                return None, 0

        alpha = -float('inf')
        beta = float('inf')
        best_move = moves[0]
        best_score = -float('inf')

        for move in moves:
            # Make move
            new_pos = self.position.copy()
            new_pos.make_move(move)

            # Search
            score = -self._alpha_beta(
                new_pos,
                depth - 1,
                -beta,
                -alpha,
                self.position.turn.opposite()
            )

            # Update best move
            if score > best_score:
                best_score = score
                best_move = move

            # Update alpha
            alpha = max(alpha, score)

            # Beta cutoff
            if alpha >= beta:
                break

        return best_move, best_score

    def _alpha_beta(
        self,
        position: Position,
        depth: int,
        alpha: float,
        beta: float,
        color: Color
    ) -> int:
        """Alpha-beta search"""
        self.nodes_searched += 1

        # Check transposition table
        hash_key = self._hash_position(position)
        entry = self.transposition_table.get(hash_key)

        if entry and entry.depth >= depth:
            if entry.flag == 'exact':
                return entry.score
            elif entry.flag == 'lower' and entry.score >= beta:
                return entry.score
            elif entry.flag == 'upper' and entry.score <= alpha:
                return entry.score

        # Leaf node
        if depth == 0:
            score = self._quiescence_search(position, alpha, beta, color)
            self._store_transposition(hash_key, score, depth, 'exact')
            return score

        # Generate moves
        moves = self._get_ordered_moves(position)

        if not moves:
            # Checkmate or stalemate
            if self._is_check(color, position):
                return -100000 + (self.position.fullmove_number - position.fullmove_number)
            else:
                return 0

        # Search moves
        best_score = -float('inf')

        for move in moves:
            new_pos = position.copy()
            new_pos.make_move(move)

            score = -self._alpha_beta(
                new_pos,
                depth - 1,
                -beta,
                -alpha,
                color.opposite()
            )

            best_score = max(best_score, score)
            alpha = max(alpha, score)

            if alpha >= beta:
                break

        # Store in transposition table
        flag = 'exact'
        if best_score <= alpha:
            flag = 'upper'
        elif best_score >= beta:
            flag = 'lower'

        self._store_transposition(hash_key, best_score, depth, flag)

        return best_score

    def _quiescence_search(
        self,
        position: Position,
        alpha: float,
        beta: float,
        color: Color
    ) -> int:
        """Quiescence search for tactical positions"""
        # Stand pat
        stand_pat = self.evaluator.evaluate(position)

        if color == Color.BLACK:
            stand_pat = -stand_pat

        if stand_pat >= beta:
            return beta
        if stand_pat > alpha:
            alpha = stand_pat

        # Generate capture moves
        moves = self._get_capture_moves(position)

        if not moves:
            return stand_pat

        for move in moves:
            new_pos = position.copy()
            new_pos.make_move(move)

            score = -self._quiescence_search(
                new_pos,
                -beta,
                -alpha,
                color.opposite()
            )

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def _get_ordered_moves(self, position: Optional[Position] = None) -> List[Move]:
        """Get ordered moves with move ordering"""
        if position is None:
            position = self.position

        movegen = MoveGenerator(position)
        moves = movegen.generate_legal_moves()

        # Order moves: captures first, then promotions, then others
        ordered_moves = []

        # Captures
        captures = [m for m in moves if self._is_capture(m, position)]
        ordered_moves.extend(captures)

        # Promotions
        promotions = [m for m in moves if m.is_promotion()]
        ordered_moves.extend(promotions)

        # Other moves
        others = [m for m in moves if not self._is_capture(m, position) and not m.is_promotion()]
        ordered_moves.extend(others)

        return ordered_moves

    def _get_capture_moves(self, position: Position) -> List[Move]:
        """Get capture moves only"""
        movegen = MoveGenerator(position)
        moves = movegen.generate_legal_moves()

        return [m for m in moves if self._is_capture(m, position)]

    def _is_capture(self, move: Move, position: Position) -> bool:
        """Check if move is a capture"""
        target_piece = position.get_piece(move.to_sq)
        return target_piece is not None

    def _is_check(self, color: Color, position: Optional[Position] = None) -> bool:
        """Check if color is in check"""
        if position is None:
            position = self.position

        movegen = MoveGenerator(position)
        return movegen.is_in_check(position, color)

    def _hash_position(self, position: Position) -> int:
        """Simple hash of position"""
        hash_val = 0

        for square in position.board:
            if square is not None:
                hash_val ^= hash(square)

        hash_val ^= hash(position.turn)
        hash_val ^= hash(position.castling)
        hash_val ^= hash(position.en_passant)

        return hash_val

    def _store_transposition(
        self,
        hash_key: int,
        score: int,
        depth: int,
        flag: str,
        move: Optional[Move] = None
    ) -> None:
        """Store position in transposition table"""
        # Limit table size
        if len(self.transposition_table) > config.TRANSPOSITION_TABLE_SIZE:
            # Remove oldest entry
            self.transposition_table.pop(next(iter(self.transposition_table)))

        entry = TranspositionEntry(hash_key, score, depth, flag, move)
        self.transposition_table[hash_key] = entry

    def get_nodes_searched(self) -> int:
        """Get number of nodes searched"""
        return self.nodes_searched

    def reset(self) -> None:
        """Reset search state"""
        self.nodes_searched = 0
        self.transposition_table.clear()