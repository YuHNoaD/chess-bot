"""
Auto login with PyAutoGUI - with screenshot for debugging
"""

import time
import pyautogui
import subprocess
from datetime import datetime

# Config
USERNAME = "YuHNoaD"
PASSWORD = "YuHNoaD06@"

# Default coordinates (may need adjustment)
USERNAME_X = 960
USERNAME_Y = 400
PASSWORD_X = 960
PASSWORD_Y = 450
LOGIN_X = 960
LOGIN_Y = 520

# Safety
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

print("="*60)
print("CHESS.COM PYAUTOGUI AUTO LOGIN")
print("="*60)

def take_screenshot(filename):
    """Take screenshot"""
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")

try:
    print("\nOpening chess.com login page...")

    # Take screenshot before opening browser
    take_screenshot("before_browser.png")

    # Open chess.com login page
    url = "https://www.chess.com/login"
    subprocess.Popen(['start', url], shell=True)

    # Wait for browser to open
    print("Waiting 5 seconds for browser to open...")
    time.sleep(5)

    # Take screenshot after opening browser
    take_screenshot("after_browser.png")

    print("[OK] Browser opened")

    print("\nWaiting 3 seconds before login...")
    time.sleep(3)

    # Take screenshot before login
    take_screenshot("before_login.png")

    print("\nAttempting login...")

    # Click username field
    print(f"Clicking username field at ({USERNAME_X}, {USERNAME_Y})...")
    pyautogui.click(USERNAME_X, USERNAME_Y)
    time.sleep(0.5)

    # Type username
    print(f"Typing username: {USERNAME}")
    pyautogui.write(USERNAME)
    time.sleep(0.5)

    # Take screenshot after typing username
    take_screenshot("after_username.png")

    # Click password field
    print(f"Clicking password field at ({PASSWORD_X}, {PASSWORD_Y})...")
    pyautogui.click(PASSWORD_X, PASSWORD_Y)
    time.sleep(0.5)

    # Type password
    print("Typing password...")
    pyautogui.write(PASSWORD)
    time.sleep(0.5)

    # Take screenshot after typing password
    take_screenshot("after_password.png")

    # Click login button
    print(f"Clicking login button at ({LOGIN_X}, {LOGIN_Y})...")
    pyautogui.click(LOGIN_X, LOGIN_Y)

    # Take screenshot after clicking login
    take_screenshot("after_login_click.png")

    print("\n[OK] Login clicked!")
    print("Wait 10 seconds to check if login was successful...")

    time.sleep(10)

    # Take final screenshot
    take_screenshot("final.png")

    print("\nAuto login completed!")
    print("Screenshots saved:")
    print("  - before_browser.png")
    print("  - after_browser.png")
    print("  - before_login.png")
    print("  - after_username.png")
    print("  - after_password.png")
    print("  - after_login_click.png")
    print("  - final.png")

except Exception as e:
    print(f"\n[ERROR] Login failed: {e}")
    import traceback
    traceback.print_exc()
    take_screenshot("error.png")
    print("Error screenshot saved: error.png")