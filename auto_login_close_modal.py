"""
Auto login with PyAutoGUI - close modal first
"""

import time
import pyautogui
import subprocess

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

# Modal close button coordinates (from screenshot - top right of modal)
MODAL_CLOSE_X = 1300
MODAL_CLOSE_Y = 300

# Safety
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

print("="*60)
print("CHESS.COM PYAUTOGUI AUTO LOGIN")
print("="*60)

try:
    print("\nOpening chess.com login page...")

    # Open chess.com login page
    url = "https://www.chess.com/login"
    subprocess.Popen(['start', url], shell=True)

    # Wait for browser to open
    print("Waiting 5 seconds for browser to open...")
    time.sleep(5)

    print("[OK] Browser opened")

    print("\nWaiting 2 seconds for page to fully load...")
    time.sleep(2)

    # Close modal if present
    print("Attempting to close modal...")
    pyautogui.click(MODAL_CLOSE_X, MODAL_CLOSE_Y)
    time.sleep(1)

    print("Waiting 1 second after closing modal...")
    time.sleep(1)

    print("\nAttempting login...")

    # Click username field
    print(f"Clicking username field at ({USERNAME_X}, {USERNAME_Y})...")
    pyautogui.click(USERNAME_X, USERNAME_Y)
    time.sleep(0.5)

    # Type username
    print(f"Typing username: {USERNAME}")
    pyautogui.write(USERNAME)
    time.sleep(0.5)

    # Click password field
    print(f"Clicking password field at ({PASSWORD_X}, {PASSWORD_Y})...")
    pyautogui.click(PASSWORD_X, PASSWORD_Y)
    time.sleep(0.5)

    # Type password
    print("Typing password...")
    pyautogui.write(PASSWORD)
    time.sleep(0.5)

    # Click login button
    print(f"Clicking login button at ({LOGIN_X}, {LOGIN_Y})...")
    pyautogui.click(LOGIN_X, LOGIN_Y)

    print("\n[OK] Login clicked!")
    print("Wait 10 seconds to check if login was successful...")

    time.sleep(10)

    print("\nAuto login completed!")
    print("If login was successful, you should be logged in to chess.com")

except Exception as e:
    print(f"\n[ERROR] Login failed: {e}")
    import traceback
    traceback.print_exc()