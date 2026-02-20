"""
ELO Farming Bot - Auto-play on chess.com
"""

import sys
import os
import time
import requests
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.search import Search
from src.evaluation import Evaluator
from src.movegen import MoveGenerator
from src.type_defs.chess_types import Color
from src.uci.uci import UCIEngine
import config_chesscom


class ChessComEloFarmer:
    """Auto-play bot for chess.com ELO farming"""

    def __init__(self, username: str, api_key: str):
        self.username = username
        self.api_key = api_key

        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        self.engine = UCIEngine()
        self.engine.connect_to_chesscom(username, api_key)

        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def get_active_games(self) -> list:
        """Get active games"""
        url = f"https://api.chess.com/pub/player/{self.username}/games"
        params = {
            'status': 'in_progress',
            'ongoing': 'true'
        }

        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            return data.get('games', [])
        else:
            print(f"[ERROR] Cannot get active games: {response.status_code}")
            return []

    def get_pending_challenges(self) -> list:
        """Get pending challenges"""
        url = f"https://api.chess.com/pub/player/{self.username}/challenges"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            return data.get('challenges', [])
        else:
            print(f"[ERROR] Cannot get challenges: {response.status_code}")
            return []

    def accept_challenge(self, challenge_id: str) -> bool:
        """Accept a challenge"""
        url = f"https://api.chess.com/pub/challenge/{challenge_id}/accept"

        response = requests.post(url, headers=self.headers)

        if response.status_code == 200:
            print(f"[OK] Accepted challenge {challenge_id}")
            return True
        else:
            print(f"[ERROR] Cannot accept challenge: {response.status_code}")
            return False

    def decline_challenge(self, challenge_id: str) -> bool:
        """Decline a challenge"""
        url = f"https://api.chess.com/pub/challenge/{challenge_id}/decline"

        response = requests.post(url, headers=self.headers)

        if response.status_code == 200:
            print(f"[OK] Declined challenge {challenge_id}")
            return True
        else:
            print(f"[ERROR] Cannot decline challenge: {response.status_code}")
            return False

    def make_move(self, game_id: str, move_str: str) -> bool:
        """Make a move in a game"""
        url = f"https://api.chess.com/pub/game/{game_id}/move"

        payload = {
            'move': move_str
        }

        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            print(f"[OK] Made move {move_str} in game {game_id}")
            return True
        else:
            print(f"[ERROR] Cannot make move: {response.status_code}")
            return False

    def get_game_state(self, game_id: str) -> dict:
        """Get game state"""
        url = f"https://api.chess.com/pub/game/{game_id}"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Cannot get game state: {response.status_code}")
            return {}

    def play_game(self, game_id: str) -> str:
        """Play a complete game, return result"""
        print(f"\n{'='*60}")
        print(f"Playing game {game_id}")
        print(f"{'='*60}")

        position = Position()
        search = Search(position)
        evaluator = Evaluator()

        moves_made = 0
        last_result = None

        while True:
            # Get game state
            game_state = self.get_game_state(game_id)

            if not game_state:
                print("[ERROR] Cannot get game state")
                break

            # Check if game is over
            game_status = game_state.get('status')
            if game_status != 'in_progress':
                print(f"\nGame over! Status: {game_status}")

                # Determine result
                if 'white' in game_state and game_state['white'].get('username') == self.username:
                    my_color = Color.WHITE
                else:
                    my_color = Color.BLACK

                result = game_state.get('result')
                if result == '1-0':
                    last_result = 'win' if my_color == Color.WHITE else 'loss'
                elif result == '0-1':
                    last_result = 'loss' if my_color == Color.WHITE else 'win'
                else:
                    last_result = 'draw'

                print(f"Result: {result} ({last_result})")
                break

            # Get FEN from game state
            fen = game_state.get('fen')

            # Check if position has changed
            if fen:
                position = Position(fen)

            # Check if it's our turn
            my_turn = False
            if 'white' in game_state and game_state['white'].get('username') == self.username:
                my_turn = (position.turn == Color.WHITE)
            else:
                my_turn = (position.turn == Color.BLACK)

            if my_turn:
                print(f"\n[TURN] {'White' if position.turn == Color.WHITE else 'Black'}")

                # Check if game over
                movegen = MoveGenerator(position)
                legal_moves = movegen.generate_legal_moves()

                if not legal_moves:
                    if movegen.is_in_check(position.turn):
                        print("CHECKMATE!")
                        last_result = 'loss'
                    else:
                        print("STALEMATE!")
                        last_result = 'draw'
                    break

                # Find best move
                print("Thinking...")
                search = Search(position)

                # Vary search depth for elo farming (sometimes play slower, sometimes faster)
                depth = random.randint(3, config_chesscom.ELO_FARMING_DEPTH)
                time_limit = random.uniform(0.5, 2.0)

                best_move = search.find_best_move(depth=depth, time_limit=time_limit)

                if best_move:
                    print(f"Best move: {best_move} (depth {depth})")
                    print(f"Nodes: {search.get_nodes_searched()}")

                    # Make move
                    if self.make_move(game_id, str(best_move)):
                        moves_made += 1
                        position.make_move(best_move)

                        # Evaluate
                        score = evaluator.evaluate(position)
                        print(f"Position score: {score:.1f}")
                    else:
                        print("[ERROR] Cannot make move")
                        break
                else:
                    print("[ERROR] No best move found")
                    break

            # Wait before next check
            time.sleep(random.uniform(1, 3))

        return last_result

    def elo_farming_loop(self, max_games: int = 100):
        """Main ELO farming loop"""
        print(f"\n{'='*60}")
        print(f"ELO FARMING BOT STARTED")
        print(f"Username: {self.username}")
        print(f"Max games: {max_games}")
        print(f"{'='*60}")

        games_played = 0

        while games_played < max_games:
            # Check for active games
            active_games = self.get_active_games()

            if active_games:
                # Play active games
                for game in active_games:
                    game_id = game.get('url', '').split('/')[-1]

                    if game_id:
                        result = self.play_game(game_id)

                        if result:
                            self.games_played += 1
                            games_played += 1

                            if result == 'win':
                                self.wins += 1
                            elif result == 'draw':
                                self.draws += 1
                            else:
                                self.losses += 1

                            print(f"\nStats: {self.wins}W - {self.draws}D - {self.losses}L")
            else:
                # No active games, check for challenges
                challenges = self.get_pending_challenges()

                if challenges:
                    # Accept challenges
                    for challenge in challenges:
                        challenge_id = challenge.get('id')

                        if challenge_id:
                            # Check if challenge is valid
                            opp_rating = challenge.get('opponent', {}).get('rating', 0)

                            # Accept if opponent rating is within range
                            min_rating = config_chesscom.MIN_OPPONENT_RATING
                            max_rating = config_chesscom.MAX_OPPONENT_RATING

                            if min_rating <= opp_rating <= max_rating:
                                print(f"\n[CHALLENGE] Accepting from {challenge.get('opponent', {}).get('username')} (rating: {opp_rating})")
                                self.accept_challenge(challenge_id)
                            else:
                                print(f"\n[CHALLENGE] Declining from {challenge.get('opponent', {}).get('username')} (rating: {opp_rating} - out of range)")
                                self.decline_challenge(challenge_id)

                            # Wait a bit
                            time.sleep(2)

            # Wait before next check
            print(f"\n[WAIT] Checking for games in {config_chesscom.CHECK_INTERVAL}s...")
            time.sleep(config_chesscom.CHECK_INTERVAL)

        # Print final stats
        print(f"\n{'='*60}")
        print(f"ELO FARMING COMPLETED")
        print(f"Games played: {self.games_played}")
        print(f"Results: {self.wins}W - {self.draws}D - {self.losses}L")
        win_rate = (self.wins / self.games_played * 100) if self.games_played > 0 else 0
        print(f"Win rate: {win_rate:.1f}%")
        print(f"{'='*60}")


def main():
    """Main function"""
    # Configuration
    username = config_chesscom.CHESSCOM_BOT_USERNAME
    api_key = config_chesscom.CHESSCOM_API_KEY

    if not username or not api_key:
        print("[ERROR] Please configure CHESSCOM_BOT_USERNAME and CHESSCOM_API_KEY in config_chesscom.py")
        print("\nTo get these:")
        print("1. Go to https://www.chess.com/club/chess-com-bots")
        print("2. Register your bot")
        print("3. Get username and API key")
        print("4. Update config_chesscom.py")
        return

    # Create farmer
    farmer = ChessComEloFarmer(username, api_key)

    # Start ELO farming
    try:
        farmer.elo_farming_loop(max_games=config_chesscom.MAX_GAMES)
    except KeyboardInterrupt:
        print("\n\n[STOP] ELO farming stopped by user")


if __name__ == "__main__":
    main()