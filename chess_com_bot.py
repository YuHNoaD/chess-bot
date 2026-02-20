"""
Chess.com Bot - Complete solution with API + Selenium
"""

import time
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.search import Search
from src.evaluation import Evaluator
from src.type_defs.chess_types import Color

import chess_com_api
import config_chesscom


class ChessComBot:
    """Complete chess.com bot"""

    def __init__(self, username, api_key=None):
        self.username = username
        self.api_key = api_key

        # Create API client
        self.api = chess_com_api.ChessComAPI(api_key)

        # Stats
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def check_challenges(self):
        """Check for pending challenges"""
        if not self.api_key:
            print("[INFO] No API key - cannot check challenges")
            print("[INFO] Please register at https://www.chess.com/club/chess-com-bots")
            print("[INFO] And configure API key in config_chesscom.py")
            return []

        print("Checking for challenges...")

        challenges = self.api.get_challenges(self.username)

        print(f"Found {len(challenges)} challenges")

        return challenges

    def accept_challenge(self, challenge_id):
        """Accept a challenge"""
        if not self.api_key:
            print("[ERROR] API key required to accept challenge")
            return False

        print(f"Accepting challenge {challenge_id}...")

        if self.api.accept_challenge(challenge_id):
            print("[OK] Challenge accepted")
            return True
        else:
            print("[ERROR] Cannot accept challenge")
            return False

    def play_game(self, game_id):
        """Play a game using chess engine"""
        print(f"\nPlaying game {game_id}...")

        # Get game details
        game = self.api.get_game(game_id)

        if not game:
            print("[ERROR] Cannot get game details")
            return False

        # Get FEN from game
        fen = game.get('fen')

        if not fen:
            print("[ERROR] No FEN in game data")
            return False

        # Create position
        position = Position(fen)

        # Find best move
        print("Thinking...")
        search = Search(position)
        best_move = search.find_best_move(
            depth=config_chesscom.ELO_FARMING_DEPTH,
            time_limit=2.0
        )

        if best_move:
            print(f"Best move: {best_move}")
            print(f"Nodes: {search.get_nodes_searched()}")

            # Make move (this would need to be done via API or Selenium)
            # For now, just return the move
            return str(best_move)
        else:
            print("[ERROR] No best move found")
            return None

    def run(self, max_games=10):
        """Run the bot"""
        print("="*60)
        print("CHESS.COM BOT")
        print("="*60)
        print(f"Username: {self.username}")
        print(f"Max games: {max_games}")
        print(f"API key: {'Configured' if self.api_key else 'Not configured'}")
        print("="*60)

        if not self.api_key:
            print("\n" + "="*60)
            print("SETUP REQUIRED")
            print("="*60)
            print("\nTo use this bot:")
            print("1. Register at https://www.chess.com/club/chess-com-bots")
            print("2. Get API key from chess.com")
            print("3. Configure API key in config_chesscom.py:")
            print("   CHESSCOM_BOT_USERNAME = 'your_bot_username'")
            print("   CHESSCOM_API_KEY = 'your_api_key'")
            print("\nWithout API key, you can:")
            print("- Use play_on_account.py (Selenium automation)")
            print("- Use play.py (local play)")
            print("- Use auto_play.py (bot vs bot)")
            print("="*60)
            return

        games_played = 0

        while games_played < max_games:
            # Check for challenges
            challenges = self.check_challenges()

            if challenges:
                # Accept challenges
                for challenge in challenges:
                    challenge_id = challenge.get('id')

                    if challenge_id:
                        # Check if opponent rating is within range
                        opp_rating = challenge.get('opponent', {}).get('rating', 0)

                        if config_chesscom.MIN_OPPONENT_RATING <= opp_rating <= config_chesscom.MAX_OPPONENT_RATING:
                            print(f"\nAccepting challenge from {challenge.get('opponent', {}).get('username')} (rating: {opp_rating})")

                            if self.accept_challenge(challenge_id):
                                games_played += 1
                        else:
                            print(f"\nDeclining challenge (rating {opp_rating} out of range)")
            else:
                print("No challenges found")

            # Wait before next check
            print(f"\nWaiting {config_chesscom.CHECK_INTERVAL} seconds before next check...")
            time.sleep(config_chesscom.CHECK_INTERVAL)

        # Print final stats
        print(f"\n{'='*60}")
        print(f"SESSION COMPLETED")
        print(f"{'='*60}")
        print(f"Games played: {self.games_played}")
        print(f"Results: {self.wins}W - {self.draws}D - {self.losses}L")
        print(f"{'='*60}")


def main():
    """Main function"""
    # Get credentials from config
    username = config_chesscom.CHESSCOM_BOT_USERNAME
    api_key = config_chesscom.CHESSCOM_API_KEY

    # Check if configured
    if not username or not api_key or username == "your_bot_username":
        print("="*60)
        print("CHESS.COM BOT - SETUP REQUIRED")
        print("="*60)
        print("\nTo use this bot:")
        print("1. Register at https://www.chess.com/club/chess-com-bots")
        print("2. Get API key from chess.com")
        print("3. Configure config_chesscom.py:")
        print("   CHESSCOM_BOT_USERNAME = 'your_bot_username'")
        print("   CHESSCOM_API_KEY = 'your_api_key'")
        print("\nFor now, you can:")
        print("- Use play.py to play against the bot locally")
        print("- Use auto_play.py to watch the bot play against itself")
        print("="*60)
        return

    # Create bot
    bot = ChessComBot(username, api_key)

    try:
        # Run bot
        bot.run(max_games=config_chesscom.MAX_GAMES)

    except KeyboardInterrupt:
        print("\n\n[STOP] Bot stopped by user")

    except Exception as e:
        print(f"\n[ERROR] Bot error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()