"""
Play on your chess.com account using undetected-chromedriver
WARNING: This violates chess.com TOS - use at your own risk!
"""

import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.evaluation.evaluation import Evaluator
from src.movegen.movegen import MoveGenerator
from src.position import Position
from src.search import Search
from src.type_defs.chess_types import Color, Square, Move

# Import config
import config_account


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
        """Setup undetected Chrome driver"""
        options = uc.ChromeOptions()

        if self.headless:
            options.add_argument('--headless')

        # Use existing Chrome profile
        user_data_dir = config_account.CHROME_USER_DATA_DIR
        profile_directory = config_account.CHROME_PROFILE_DIRECTORY

        if user_data_dir and profile_directory:
            print(f"[INFO] Using Chrome profile: {user_data_dir}\\{profile_directory}")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument(f'--profile-directory={profile_directory}')
        else:
            print("[INFO] Using default Chrome profile")

        # Anti-detection options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Fix ChromeDriver version issue
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')

        try:
            self.driver = uc.Chrome(options=options, version_main=144)
        except Exception as e:
            print(f"[ERROR] Cannot create Chrome driver: {e}")
            raise

    def login(self):
        """Login to chess.com (or check if already logged in)"""
        print("Checking login status...")

        # Go to chess.com homepage
        self.driver.get("https://www.chess.com")

        # Wait for page to load
        time.sleep(5)

        # Check if already logged in
        try:
            # Look for user menu or username in the page
            user_menu = self.driver.find_elements(By.CSS_SELECTOR, "[data-cy='user-menu']")
            username_element = self.driver.find_elements(By.CSS_SELECTOR, "[data-cy='user-username']")

            if user_menu or username_element:
                print("[OK] Already logged in!")
                print(f"[INFO] Using existing Chrome profile with saved login")
                return True
        except:
            pass

        # If not logged in, try to login
        print("Not logged in - attempting login...")

        # Go to login page
        self.driver.get("https://www.chess.com/login")

        # Wait for page to load
        time.sleep(10)

        try:
            # Close cookie banner if present
            try:
                cookie_accept = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Accept cookies']"))
                )
                cookie_accept.click()
                print("[INFO] Closed cookie banner")
                time.sleep(2)
            except:
                pass

            # Close any modal if present
            try:
                close_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Close']")
                if close_buttons:
                    for btn in close_buttons:
                        try:
                            btn.click()
                            print("[INFO] Closed modal")
                            time.sleep(1)
                        except:
                            pass
            except:
                pass

            # Try multiple selectors for username field
            username_field = None
            selectors = [
                (By.ID, "username"),
                (By.NAME, "username"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.XPATH, "//input[@placeholder='Username']"),
                (By.XPATH, "//input[@name='username']"),
            ]

            for selector in selectors:
                try:
                    username_field = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[INFO] Found username field using selector: {selector}")
                    break
                except:
                    continue

            if not username_field:
                print("[ERROR] Cannot find username field!")
                return False

            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_field)
            time.sleep(1)

            # Wait for element to be visible and clickable
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of(username_field)
            )

            # Click on username field first
            username_field.click()
            time.sleep(0.5)

            # Clear and enter username
            username_field.clear()
            username_field.send_keys(self.username)
            print(f"[INFO] Entered username: {self.username}")
            time.sleep(0.5)

            # Try multiple selectors for password field
            password_field = None
            password_selectors = [
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.XPATH, "//input[@placeholder='Password']"),
                (By.XPATH, "//input[@name='password']"),
            ]

            for selector in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[INFO] Found password field using selector: {selector}")
                    break
                except:
                    continue

            if not password_field:
                print("[ERROR] Cannot find password field!")
                return False

            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_field)
            time.sleep(1)

            # Wait for element to be visible
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of(password_field)
            )

            # Click on password field first
            password_field.click()
            time.sleep(0.5)

            # Clear field
            password_field.clear()
            time.sleep(0.3)

            # Enter password
            password_field.send_keys(self.password)
            print("[INFO] Entered password")
            time.sleep(0.5)

            # Take screenshot before login
            self.driver.save_screenshot("before_login.png")
            print("[INFO] Screenshot saved: before_login.png")

            # Try multiple selectors for login button
            login_button = None
            button_selectors = [
                (By.ID, "login"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Log In')]"),
                (By.XPATH, "//button[contains(text(), 'Login')]"),
                (By.CSS_SELECTOR, "button.login"),
            ]

            for selector in button_selectors:
                try:
                    login_button = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located(selector)
                    )
                    print(f"[INFO] Found login button using selector: {selector}")
                    break
                except:
                    continue

            if not login_button:
                print("[ERROR] Cannot find login button!")
                return False

            # Scroll to button
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_button)
            time.sleep(1)

            # Wait for element to be clickable
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(login_button)
            )

            # Click login button using JavaScript
            self.driver.execute_script("arguments[0].click();", login_button)
            print("[INFO] Clicked login button")

            # Wait for redirect
            time.sleep(5)

            # Check if login successful by checking URL
            if "chess.com/login" in self.driver.current_url:
                print("[ERROR] Login failed - still on login page")
                # Take screenshot for debugging
                self.driver.save_screenshot("login_error.png")
                print("[INFO] Screenshot saved to login_error.png")
                return False

            print("[OK] Logged in successfully!")
            return True

        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            import traceback
            traceback.print_exc()
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot("login_error.png")
                print("[INFO] Screenshot saved to login_error.png")
            except:
                pass
            return False

    def find_game(self):
        """Find a game to play"""
        print("Looking for a game...")

        try:
            # Go to play page
            self.driver.get("https://www.chess.com/play")

            # Wait for page to load
            time.sleep(5)

            # Look for "Play" button
            play_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='play-button']"))
            )
            play_button.click()
            print("[OK] Started new game")

            # Wait for game to load
            time.sleep(5)

            return True

        except Exception as e:
            print(f"[ERROR] Cannot find game: {e}")
            return False

    def get_board_position(self):
        """Get current board position from chess.com"""
        # This is a simplified version - you'll need to implement
        # actual board parsing from chess.com UI
        return Position()

    def make_move(self, move: Move):
        """Make a move on chess.com"""
        # This is a simplified version - you'll need to implement
        # actual move making on chess.com UI
        pass

    def play_game(self):
        """Play a single game"""
        print("Playing game...")

        try:
            # Find and start game
            if not self.find_game():
                return False

            # Play game loop
            while True:
                # Get board position
                pos = self.get_board_position()

                # Find best move
                search = Search(pos)
                best_move = search.find_best_move(depth=5, time_limit=2.0)

                if best_move:
                    print(f"Best move: {best_move}")
                    search_nodes = search.get_nodes_searched()
                    print(f"Nodes searched: {search_nodes}")

                    # Make move
                    self.make_move(best_move)
                else:
                    print("No legal moves!")
                    break

                # Wait for opponent
                time.sleep(2)

        except Exception as e:
            print(f"[ERROR] Game error: {e}")
            return False

    def run(self, max_games: int = 10):
        """Run bot for multiple games"""
        print("=" * 60)
        print("CHESS.COM ACCOUNT BOT")
        print("=" * 60)
        print(f"[INFO] Using account: {self.username}")
        print(f"[INFO] Max games: {max_games}")
        print(f"[INFO] Headless: {self.headless}")
        print()

        try:
            # Setup driver
            self.setup_driver()

            # Login
            if not self.login():
                print("[ERROR] Login failed!")
                return

            # Play games
            for game_num in range(1, max_games + 1):
                print(f"\nGame {game_num}/{max_games}")
                print("-" * 60)

                if self.play_game():
                    self.games_played += 1
                    print(f"[OK] Game {game_num} completed")
                else:
                    print(f"[ERROR] Game {game_num} failed")

                # Wait between games
                if game_num < max_games:
                    time.sleep(10)

            # Print stats
            print("\n" + "=" * 60)
            print("FINAL STATS")
            print("=" * 60)
            print(f"Games played: {self.games_played}")
            print(f"Wins: {self.wins}")
            print(f"Draws: {self.draws}")
            print(f"Losses: {self.losses}")

        except KeyboardInterrupt:
            print("\n[INFO] Bot stopped by user")
        except Exception as e:
            print(f"[ERROR] Bot error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Close browser
            try:
                self.driver.quit()
                print("[OK] Browser closed")
            except:
                pass


def main():
    """Main entry point"""
    # Create bot
    bot = ChessComAccountBot(
        username=config_account.CHESSCOM_USERNAME,
        password=config_account.CHESSCOM_PASSWORD,
        headless=False
    )

    # Run bot
    bot.run(max_games=10)


if __name__ == "__main__":
    main()