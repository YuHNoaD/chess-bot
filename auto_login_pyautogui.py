"""
Auto login with PyAutoGUI using default coordinates
"""

import time
import pyautogui
import subprocess

# Config
USERNAME = "YuHNoaD"
PASSWORD = "YuHNoaD06@"

# Default coordinates (may need adjustment)
USERNAME_X = 500
USERNAME_Y = 400
PASSWORD_X = 500
PASSWORD_Y = 450
LOGIN_X = 500
LOGIN_Y = 520

# Safety
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

print("="*60)
print("CHESS.COM PYAUTOGUI AUTO LOGIN")
print("="*60)

print("\nOpening chess.com login page...")

# Open chess.com login page
url = "https://www.chess.com/login"
subprocess.Popen(['start', url], shell=True)

# Wait for browser to open
time.sleep(5)

print("[OK] Browser opened")

print("\nWaiting 3 seconds before login...")
time.sleep(3)

print("\nAttempting login...")

# Click username field
print("Clicking username field...")
pyautogui.click(USERNAME_X, USERNAME_Y)
time.sleep(0.5)

# Type username
print(f"Typing username: {USERNAME}")
pyautogui.write(USERNAME)
time.sleep(0.5)

# Click password field
print("Clicking password field...")
pyautogui.click(PASSWORD_X, PASSWORD_Y)
time.sleep(0.5)

# Type password
print("Typing password...")
pyautogui.write(PASSWORD)
time.sleep(0.5)

# Click login button
print("Clicking login button...")
pyautogui.click(LOGIN_X, LOGIN_Y)

print("\n[OK] Login clicked!")
print("Wait 10 seconds to check if login was successful...")

time.sleep(10)

print("\nAuto login completed!")
print("If login was successful, you should be logged in to chess.com")
print("\nIf login failed, you may need to adjust the coordinates in this script")