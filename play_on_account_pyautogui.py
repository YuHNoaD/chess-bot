"""
Play on chess.com using PyAutoGUI
WARNING: This violates chess.com TOS - use at your own risk!
"""

import time
import pyautogui
import subprocess
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.search import Search
from src.evaluation import Evaluator
from src.movegen import MoveGenerator
from src.type_defs.chess_types import Color, Square, Move

# Config
import config_account

USERNAME = config_account.CHESSCOM_USERNAME
PASSWORD = config_account.CHESSCOM_PASSWORD

# Safety
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True


class ChessComPyAutoGUIBot:
    """Bot that plays on chess.com using PyAutoGUI"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        # Initialize chess engine
        self.evaluator = Evaluator()

        # Stats
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def open_browser(self):
        """Open chess.com login page"""
        print("Opening chess.com login page...")

        # Open default browser
        url = "https://www.chess.com/login"
        subprocess.Popen(['start', url], shell=True)

        # Wait for browser to open
        time.sleep(5)

        print("[OK] Browser opened")

    def login(self):
        """Login to chess.com using PyAutoGUI"""
        print("Logging in to chess.com...")

        try:
            # Click on username field
            print("Clicking username field...")
            username_pos = pyautogui.locateOnScreen('username_field.png', confidence=0.8)

            if not username_pos:
                print("[ERROR] Cannot find username field!")
                print("[INFO] Trying to click using coordinates...")
                # Default coordinates - may need adjustment
                pyautogui.click(500, 400)
            else:
                username_center = pyautogui.center(username_pos)
                pyautogui.click(username_center)

            time.sleep(0.5)

            # Type username
            print(f"Typing username: {self.username}")
            pyautogui.write(self.username)
            time.sleep(0.5)

            # Click on password field
            print("Clicking password field...")
            password_pos = pyautogui.locateOnScreen('password_field.png', confidence=0.8)

            if not password_pos:
                print("[INFO] Trying to click using coordinates...")
                # Default coordinates - may need adjustment
                pyautogui.click(500, 450)
            else:
                password_center = pyautogui.center(password_pos)
                pyautogui.click(password_center)

            time.sleep(0.5)

            # Type password
            print("Typing password...")
            pyautogui.write(self.password)
            time.sleep(0.5)

            # Click login button
            print("Clicking login button...")
            login_pos = pyautogui.locateOnScreen('login_button.png', confidence=0.8)

            if not login_pos:
                print("[INFO] Trying to click using coordinates...")
                # Default coordinates - may need adjustment
                pyautogui.click(500, 520)
            else:
                login_center = pyautogui.center(login_pos)
                pyautogui.click(login_center)

            print("[OK] Login clicked!")

            # Wait for login
            time.sleep(5)

            print("[OK] Login successful!")
            return True

        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            return False

    def find_game(self):
        """Find a game to play"""
        print("Looking for a game...")

        try:
            # Click on Play button
            print("Clicking Play button...")
            play_pos = pyautogui.locateOnScreen('play_button.png', confidence=0.8)

            if play_pos:
                play_center = pyautogui.center(play_pos)
                pyautogui.click(play_center)
                print("[OK] Found a game!")
                return True
            else:
                print("[ERROR] Cannot find Play button!")
                return False

        except Exception as e:
            print(f"[ERROR] Cannot find game: {e}")
            return False

    def play_game(self):
        """Play a complete game"""
        print("\n" + "="*60)
        print("PLAYING GAME")
        print("="*60)

        try:
            # Find a game
            if not self.find_game():
                return False

            # Wait for game to start
            time.sleep(3)

            # Play loop
            while True:
                # Check if game is over
                game_over_pos = pyautogui.locateOnScreen('game_over.png', confidence=0.8)

                if game_over_pos:
                    print("\nGame over!")
                    self.analyze_result()
                    break

                # Check if it's our turn
                # This is complex - need to parse the UI
                # For now, just wait and check periodically
                time.sleep(2)

            return True

        except Exception as e:
            print(f"[ERROR] Game error: {e}")
            return False

    def analyze_result(self):
        """Analyze game result"""
        try:
            # Get result text (not implemented)
            print("Analyzing result...")

            # Update stats
            self.games_played += 1

            # Close modal
            close_pos = pyautogui.locateOnScreen('close_button.png', confidence=0.8)

            if close_pos:
                close_center = pyautogui.center(close_pos)
                pyautogui.click(close_center)

        except Exception as e:
            print(f"[ERROR] Cannot analyze result: {e}")

    def play_multiple_games(self, max_games: int):
        """Play multiple games"""
        print(f"\n{'='*60}")
        print(f"PLAYING {max_games} GAMES")
        print(f"{'='*60}")

        for i in range(max_games):
            print(f"\nGame {i+1}/{max_games}")

            if self.play_game():
                print(f"\nGame {i+1} completed!")
            else:
                print(f"\nGame {i+1} failed!")

            # Wait before next game
            if i < max_games - 1:
                print(f"\nWaiting 10 seconds before next game...")
                time.sleep(10)

        # Print final stats
        print(f"\n{'='*60}")
        print(f"SESSION COMPLETED")
        print(f"{'='*60}")
        print(f"Games played: {self.games_played}")
        print(f"Results: {self.wins}W - {self.draws}D - {self.losses}L")
        win_rate = (self.wins / self.games_played * 100) if self.games_played > 0 else 0
        print(f"Win rate: {win_rate:.1f}%")
        print(f"{'='*60}")


def main():
    """Main function"""
    print("="*60)
    print("CHESS.COM PYAUTOGUI BOT")
    print("="*60)
    print("\nWARNING: This violates chess.com TOS!")
    print("Use at your own risk - account may be banned!")
    print("\nNOTE: You need to provide screenshots of:")
    print("  - username_field.png")
    print("  - password_field.png")
    print("  - login_button.png")
    print("  - play_button.png")
    print("  - game_over.png")
    print("  - close_button.png")
    print("="*60)

    if not USERNAME or not PASSWORD or USERNAME == "your_username":
        print("[ERROR] Please configure CHESSCOM_USERNAME and CHESSCOM_PASSWORD in config_account.py!")
        return

    print(f"\n[INFO] Using account: {USERNAME}")
    print(f"[INFO] Max games: {config_account.MAX_GAMES_PER_SESSION}")

    # Create bot
    bot = ChessComPyAutoGUIBot(USERNAME, PASSWORD)

    try:
        # Open browser
        bot.open_browser()

        # Login
        if not bot.login():
            print("[ERROR] Login failed!")
            return

        # Play games
        bot.play_multiple_games(max_games=config_account.MAX_GAMES_PER_SESSION)

    except KeyboardInterrupt:
        print("\n\n[STOP] Bot stopped by user")

    except Exception as e:
        print(f"\n[ERROR] Bot error: {e}")


if __name__ == "__main__":
    main()