"""
Play on your chess.com account using Selenium
WARNING: This violates chess.com TOS - use at your own risk!
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.position import Position
from src.search import Search
from src.evaluation import Evaluator
from src.movegen import MoveGenerator
from src.type_defs.chess_types import Color, Square, Move


class ChessComAccountBot:
    """Bot that plays on your chess.com account"""

    def __init__(self, username: str, password: str, headless: bool = False):
        self.username = username
        self.password = password
        self.headless = headless

        # Initialize chess engine
        self.evaluator = Evaluator()

        # Stats
        self.games_played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def setup_driver(self):
        """Setup Selenium Chrome driver"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        # Anti-detection options
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        """Login to chess.com"""
        print("Logging in to chess.com...")

        # Go to login page
        self.driver.get("https://www.chess.com/login")

        # Wait for page to load
        wait = WebDriverWait(self.driver, 10)

        try:
            # Enter username
            username_field = wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.clear()
            username_field.send_keys(self.username)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(self.password)

            # Click login button
            login_button = self.driver.find_element(By.ID, "login")
            login_button.click()

            # Wait for redirect
            time.sleep(3)

            print("[OK] Logged in successfully!")
            return True

        except TimeoutException:
            print("[ERROR] Login timeout!")
            return False
        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            return False

    def find_game(self):
        """Find a game to play"""
        print("Looking for a game...")

        try:
            # Go to play page
            self.driver.get("https://www.chess.com/play/online")

            # Wait for page to load
            time.sleep(2)

            # Click on "Play" button for random opponent
            play_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Play')]"))
            )
            play_button.click()

            print("[OK] Found a game!")
            return True

        except Exception as e:
            print(f"[ERROR] Cannot find game: {e}")
            return False

    def get_current_position(self) -> Position:
        """Get current position from the board"""
        try:
            # This is complex - need to parse the board from HTML
            # For now, return None (not implemented)
            return None
        except Exception as e:
            print(f"[ERROR] Cannot get position: {e}")
            return None

    def make_move_selenium(self, move: Move) -> bool:
        """Make a move using Selenium"""
        try:
            # Find source and target squares
            from_sq = move.from_sq
            to_sq = move.to_sq

            # Click source square
            source_element = self.driver.find_element(
                By.XPATH,
                f"//div[@data-square='{str(from_sq)}']"
            )
            source_element.click()
            time.sleep(random.uniform(0.1, 0.3))

            # Click target square
            target_element = self.driver.find_element(
                By.XPATH,
                f"//div[@data-square='{str(to_sq)}']"
            )
            target_element.click()

            print(f"[OK] Made move: {move}")
            return True

        except NoSuchElementException:
            print(f"[ERROR] Cannot find squares for move {move}")
            return False
        except Exception as e:
            print(f"[ERROR] Cannot make move: {e}")
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
                game_over_element = self.driver.find_elements(By.CLASS_NAME, "game-over-modal")

                if game_over_element:
                    print("\nGame over!")
                    self.analyze_result()
                    break

                # Check if it's our turn
                # This is complex - need to parse the UI
                # For now, just wait and check periodically
                time.sleep(2)

                # Get current position (not implemented)
                position = self.get_current_position()

                if position is None:
                    print("[INFO] Cannot get position, skipping...")
                    continue

                # Check if it's our turn
                # Need to implement this
                # For now, assume it's our turn

                # Find best move
                search = Search(position)
                depth = random.randint(3, 5)
                time_limit = random.uniform(1, 2)

                best_move = search.find_best_move(depth=depth, time_limit=time_limit)

                if best_move:
                    # Make move with human-like timing
                    think_time = random.uniform(1, 3)
                    print(f"Thinking for {think_time:.1f}s...")
                    time.sleep(think_time)

                    # Make move
                    if self.make_move_selenium(best_move):
                        # Wait for opponent's move
                        time.sleep(random.uniform(2, 5))
                    else:
                        print("[ERROR] Cannot make move")
                        break
                else:
                    print("[ERROR] No best move found")
                    break

                # Check if game is over again
                game_over_element = self.driver.find_elements(By.CLASS_NAME, "game-over-modal")
                if game_over_element:
                    print("\nGame over!")
                    self.analyze_result()
                    break

            return True

        except Exception as e:
            print(f"[ERROR] Game error: {e}")
            return False

    def analyze_result(self):
        """Analyze game result"""
        try:
            # Find result text
            result_element = self.driver.find_element(By.CLASS_NAME, "game-over-modal")
            result_text = result_element.text

            print(f"Result: {result_text}")

            # Simple result parsing
            if "won" in result_text.lower():
                self.wins += 1
            elif "draw" in result_text.lower():
                self.draws += 1
            else:
                self.losses += 1

            self.games_played += 1

            print(f"Stats: {self.wins}W - {self.draws}D - {self.losses}L")

        except Exception as e:
            print(f"[ERROR] Cannot analyze result: {e}")

    def play_multiple_games(self, max_games: int = 10):
        """Play multiple games"""
        print("\n" + "="*60)
        print(f"PLAYING {max_games} GAMES")
        print("="*60)

        for i in range(max_games):
            print(f"\nGame {i+1}/{max_games}")

            if self.play_game():
                # Wait between games
                wait_time = random.uniform(30, 60)
                print(f"Waiting {wait_time:.0f}s before next game...")
                time.sleep(wait_time)
            else:
                print("[ERROR] Game failed")
                break

        # Print final stats
        print("\n" + "="*60)
        print("FINAL STATS")
        print("="*60)
        print(f"Games played: {self.games_played}")
        print(f"Results: {self.wins}W - {self.draws}D - {self.losses}L")
        if self.games_played > 0:
            win_rate = (self.wins / self.games_played * 100)
            print(f"Win rate: {win_rate:.1f}%")

    def close(self):
        """Close browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print("[OK] Browser closed")


def main():
    """Main function"""
    print("="*60)
    print("CHESS.COM ACCOUNT BOT")
    print("="*60)
    print("\nWARNING: This violates chess.com TOS!")
    print("Use at your own risk - account may be banned!")
    print("="*60)

    # Get credentials
    username = input("\nEnter chess.com username: ").strip()
    password = input("Enter chess.com password: ").strip()

    if not username or not password:
        print("[ERROR] Username and password required!")
        return

    # Configure
    headless = input("Run headless? (y/n): ").strip().lower() == 'y'
    max_games = int(input("How many games to play? (default: 5): ").strip() or "5")

    # Create bot
    bot = ChessComAccountBot(username, password, headless)

    try:
        # Setup
        bot.setup_driver()

        # Login
        if not bot.login():
            print("[ERROR] Login failed!")
            return

        # Play games
        bot.play_multiple_games(max_games=max_games)

    except KeyboardInterrupt:
        print("\n\n[STOP] Bot stopped by user")

    except Exception as e:
        print(f"\n[ERROR] Bot error: {e}")

    finally:
        bot.close()


if __name__ == "__main__":
    main()