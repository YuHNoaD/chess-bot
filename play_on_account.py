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
        """Setup undetected Chrome driver"""
        options = uc.ChromeOptions()

        if self.headless:
            options.add_argument('--headless')

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
        """Login to chess.com"""
        print("Logging in to chess.com...")

        # Go to login page
        self.driver.get("https://www.chess.com/login")

        # Wait for page to load
        time.sleep(5)

        try:
            # Close cookie banner if present
            try:
                cookie_accept = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Accept cookies']")
                cookie_accept.click()
                print("[INFO] Closed cookie banner")
                time.sleep(1)
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

                if position:
                    # Find best move
                    search = Search(position)
                    best_move = search.find_best_move(depth=5, time_limit=2.0)

                    if best_move:
                        # Make move
                        if self.make_move_selenium(best_move):
                            print(f"Made move: {best_move}")
                        else:
                            print("Cannot make move!")
                    else:
                        print("No best move found!")

            return True

        except Exception as e:
            print(f"[ERROR] Game error: {e}")
            return False

    def analyze_result(self):
        """Analyze game result"""
        try:
            # Get result text
            result_element = self.driver.find_element(By.CLASS_NAME, "game-over-modal")
            result_text = result_element.text

            print(f"Result: {result_text}")

            # Update stats
            if "won" in result_text.lower():
                self.wins += 1
            elif "lost" in result_text.lower():
                self.losses += 1
            else:
                self.draws += 1

            self.games_played += 1

            print(f"Stats: {self.wins}W - {self.draws}D - {self.losses}L")

            # Close modal
            close_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
            close_button.click()

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
                print(f"\nWaiting {10} seconds before next game...")
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

    def close(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
                print("[OK] Browser closed")
        except Exception as e:
            print(f"[WARN] Error closing browser: {e}")
            try:
                if self.driver:
                    self.driver.service.stop()
            except:
                pass


def main():
    """Main function"""
    print("="*60)
    print("CHESS.COM ACCOUNT BOT")
    print("="*60)
    print("\nWARNING: This violates chess.com TOS!")
    print("Use at your own risk - account may be banned!")
    print("="*60)

    # Import config
    import config_account

    # Get credentials from config
    username = config_account.CHESSCOM_USERNAME
    password = config_account.CHESSCOM_PASSWORD

    if not username or not password or username == "your_username":
        print("[ERROR] Please configure CHESSCOM_USERNAME and CHESSCOM_PASSWORD in config_account.py!")
        return

    print(f"\n[INFO] Using account: {username}")

    # Configure
    headless = config_account.HEADLESS
    max_games = config_account.MAX_GAMES_PER_SESSION

    print(f"[INFO] Max games: {max_games}")
    print(f"[INFO] Headless: {headless}")

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