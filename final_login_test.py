"""
Final PyAutoGUI login test - with multiple coordinates
"""

import time
import pyautogui
import subprocess

# Config
USERNAME = "YuHNoaD"
PASSWORD = "YuHNoaD06@"

# Safety
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

print("="*60)
print("CHESS.COM PYAUTOGUI FINAL LOGIN TEST")
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

    # Try to close modal (multiple attempts)
    print("Attempting to close modal (multiple attempts)...")

    # Try different positions for close button
    modal_close_positions = [
        (1300, 300),  # Top right of modal
        (1400, 300),  # Further right
        (1250, 300),  # Slightly left
        (1300, 250),  # Slightly up
        (1300, 350),  # Slightly down
    ]

    for i, (x, y) in enumerate(modal_close_positions):
        print(f"  Attempt {i+1}: Clicking at ({x}, {y})...")
        pyautogui.click(x, y)
        time.sleep(0.3)

    print("Waiting 1 second after closing modal...")
    time.sleep(1)

    print("\nAttempting login...")

    # Try different positions for username field
    username_positions = [
        (960, 400),  # Center
        (800, 400),  # Left
        (1100, 400),  # Right
        (960, 380),  # Up
        (960, 420),  # Down
    ]

    username_clicked = False
    for i, (x, y) in enumerate(username_positions):
        print(f"  Attempt {i+1}: Clicking username field at ({x}, {y})...")
        pyautogui.click(x, y)
        time.sleep(0.3)

        # Try to type username
        pyautogui.write('test', interval=0.05)
        time.sleep(0.3)

        # Check if text was entered (by selecting all and checking)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)

        # Clear and try next position
        pyautogui.press('backspace')
        time.sleep(0.2)

    # Type username
    print(f"Typing username: {USERNAME}")
    pyautogui.write(USERNAME)
    time.sleep(0.5)

    # Try different positions for password field
    password_positions = [
        (960, 450),  # Center
        (800, 450),  # Left
        (1100, 450),  # Right
        (960, 430),  # Up
        (960, 470),  # Down
    ]

    for i, (x, y) in enumerate(password_positions):
        print(f"  Attempt {i+1}: Clicking password field at ({x}, {y})...")
        pyautogui.click(x, y)
        time.sleep(0.3)

        # Try to type password
        pyautogui.write('test', interval=0.05)
        time.sleep(0.3)

        # Check if text was entered
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.2)

        # Clear and try next position
        pyautogui.press('backspace')
        time.sleep(0.2)

    # Type password
    print("Typing password...")
    pyautogui.write(PASSWORD)
    time.sleep(0.5)

    # Try different positions for login button
    login_positions = [
        (960, 520),  # Center
        (800, 520),  # Left
        (1100, 520),  # Right
        (960, 500),  # Up
        (960, 540),  # Down
    ]

    for i, (x, y) in enumerate(login_positions):
        print(f"  Attempt {i+1}: Clicking login button at ({x}, {y})...")
        pyautogui.click(x, y)
        time.sleep(0.5)

    print("\n[OK] Login attempts completed!")
    print("Wait 10 seconds to check if login was successful...")

    time.sleep(10)

    print("\nFinal test completed!")
    print("If login was successful, you should be logged in to chess.com")

except Exception as e:
    print(f"\n[ERROR] Login failed: {e}")
    import traceback
    traceback.print_exc()