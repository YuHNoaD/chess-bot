"""
UCI protocol implementation
Similar to Stockfish's uci.{h,cpp}
"""

import sys
import time
import requests
from typing import Optional, Dict

from ..position import Position
from ..types.chess_types import Color, Square, Move, MoveFlag
from ..search import Search
import config


class UCIEngine:
    """UCI chess engine"""

    def __init__(self):
        self.position = Position()
        self.search = None
        self.running = True
        self.debug = config.DEBUG_MODE

    def run(self) -> None:
        """Run UCI engine loop"""
        while self.running:
            try:
                line = sys.stdin.readline().strip()

                if not line:
                    continue

                self.handle_command(line)

            except KeyboardInterrupt:
                break
            except Exception as e:
                if self.debug:
                    print(f"Error: {e}", file=sys.stderr)

    def handle_command(self, command: str) -> None:
        """Handle UCI command"""
        parts = command.split()
        cmd = parts[0].lower() if parts else ""

        if cmd == "uci":
            self.uci()
        elif cmd == "isready":
            self.isready()
        elif cmd == "ucinewgame":
            self.ucinewgame()
        elif cmd == "position":
            self.position_cmd(parts[1:])
        elif cmd == "go":
            self.go_cmd(parts[1:])
        elif cmd == "stop":
            self.stop_cmd()
        elif cmd == "quit":
            self.quit_cmd()
        elif cmd == "debug":
            self.debug_cmd(parts[1:])
        elif cmd == "setoption":
            self.setoption_cmd(parts[1:])
        else:
            if self.debug:
                print(f"Unknown command: {command}", file=sys.stderr)

    def uci(self) -> None:
        """Handle uci command"""
        print("id name ChessBot 1.0")
        print("id author YuHNoaD")
        print("option name Hash type spin default 128 min 1 max 1024")
        print("option name Threads type spin default 4 min 1 max 16")
        print("option name Skill Level type spin default 10 min 0 max 20")
        print("uciok")

    def isready(self) -> None:
        """Handle isready command"""
        print("readyok")

    def ucinewgame(self) -> None:
        """Handle ucinewgame command"""
        self.position = Position()
        self.search = None

    def position_cmd(self, args: list) -> None:
        """Handle position command"""
        if not args:
            return

        if args[0] == "startpos":
            self.position = Position()
            args = args[1:]
        elif args[0] == "fen":
            fen_str = " ".join(args[1:7])
            self.position = Position(fen_str)
            args = args[7:]

        # Apply moves
        if args and args[0] == "moves":
            for move_str in args[1:]:
                move = self._parse_move(move_str)
                if move:
                    self.position.make_move(move)

    def go_cmd(self, args: list) -> None:
        """Handle go command"""
        # Parse arguments
        depth = config.SEARCH_DEPTH
        time_limit = config.SEARCH_TIME

        i = 0
        while i < len(args):
            if args[i] == "depth":
                if i + 1 < len(args):
                    depth = int(args[i + 1])
                    i += 2
            elif args[i] == "movetime":
                if i + 1 < len(args):
                    time_limit = int(args[i + 1]) / 1000.0
                    i += 2
            elif args[i] == "wtime":
                i += 2
            elif args[i] == "btime":
                i += 2
            elif args[i] == "winc":
                i += 2
            elif args[i] == "binc":
                i += 2
            elif args[i] == "movestogo":
                i += 2
            elif args[i] == "infinite":
                i += 1
            else:
                i += 1

        # Find best move
        self.search = Search(self.position)
        best_move = self.search.find_best_move(depth, time_limit)

        if best_move:
            print(f"bestmove {best_move}")
        else:
            # No legal moves
            if self.search._is_check(self.position.turn):
                print("bestmove (none)")
            else:
                print("bestmove (none)")  # Stalemate

    def stop_cmd(self) -> None:
        """Handle stop command"""
        # Stop search (not implemented for simplicity)
        pass

    def quit_cmd(self) -> None:
        """Handle quit command"""
        self.running = False

    def debug_cmd(self, args: list) -> None:
        """Handle debug command"""
        if args and args[0] == "on":
            self.debug = True
        elif args and args[0] == "off":
            self.debug = False

    def setoption_cmd(self, args: list) -> None:
        """Handle setoption command"""
        if not args:
            return

        if args[0] == "name":
            i = 1
            while i < len(args) and args[i] != "value":
                i += 1

            if i < len(args) and args[i] == "value":
                option_name = " ".join(args[1:i])
                option_value = args[i + 1] if i + 1 < len(args) else None

                # Set option
                if option_name == "Hash":
                    config.TRANSPOSITION_TABLE_SIZE = int(option_value) * 1024
                elif option_name == "Threads":
                    config.UCI_THREADS = int(option_value)
                elif option_name == "Skill Level":
                    config.UCI_SKILL_LEVEL = int(option_value)

    def _parse_move(self, move_str: str) -> Optional[Move]:
        """Parse move string to Move object"""
        if len(move_str) < 4:
            return None

        from_sq = Square.from_string(move_str[0:2])
        to_sq = Square.from_string(move_str[2:4])

        flag = MoveFlag.NORMAL
        promotion = None

        if len(move_str) > 4:
            promo_char = move_str[4].lower()
            promo_map = {
                'q': MoveFlag.PROMOTION,
                'r': MoveFlag.PROMOTION,
                'b': MoveFlag.PROMOTION,
                'n': MoveFlag.PROMOTION,
            }
            flag = promo_map.get(promo_char, MoveFlag.NORMAL)

            if flag == MoveFlag.PROMOTION:
                from ..types import PieceType
                piece_map = {
                    'q': PieceType.QUEEN,
                    'r': PieceType.ROOK,
                    'b': PieceType.BISHOP,
                    'n': PieceType.KNIGHT,
                }
                promotion = piece_map.get(promo_char)

        return Move(from_sq, to_sq, flag, promotion)

    def connect_to_chesscom(
        self,
        username: str,
        api_key: str
    ) -> None:
        """Connect to chess.com API"""
        self.chesscom_username = username
        self.chesscom_api_key = api_key

        print(f"Connected to chess.com as {username}")

    def play_chesscom_game(self, game_id: str) -> None:
        """Play a game on chess.com"""
        url = f"{config.CHESSCOM_API_URL}/pub/game/{game_id}"
        headers = {
            'Authorization': f'Bearer {self.chesscom_api_key}'
        }

        while True:
            # Get game state
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error getting game state: {response.status_code}")
                break

            game_data = response.json()
            fen = game_data.get('fen')

            if not fen:
                break

            # Update position
            self.position = Position(fen)

            # Check if it's our turn
            if self.position.turn == Color.WHITE:
                # Find best move
                self.search = Search(self.position)
                best_move = self.search.find_best_move()

                if best_move:
                    # Send move to chess.com
                    move_url = f"{config.CHESSCOM_API_URL}/pub/game/{game_id}/move"
                    move_data = {'move': str(best_move)}

                    response = requests.post(move_url, json=move_data, headers=headers)
                    if response.status_code != 200:
                        print(f"Error sending move: {response.status_code}")
                        break

            # Check if game is over
            if self.position.is_game_over():
                break

            # Wait
            time.sleep(1)