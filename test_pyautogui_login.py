"""
Simple test login with PyAutoGUI
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
print("CHESS.COM PYAUTOGUI LOGIN TEST")
print("="*60)

print("\nOpening chess.com login page...")

# Open chess.com login page
url = "https://www.chess.com/login"
subprocess.Popen(['start', url], shell=True)

# Wait for browser to open
time.sleep(5)

print("[OK] Browser opened")

print("\nInstructions:")
print("1. Make sure the chess.com login page is visible")
print("2. Position your mouse cursor on the username field")
print("3. Press Enter when ready")
print("4. Move mouse to show where to click")

input("\nPress Enter when ready...")

print("\nCurrent mouse position:")
x, y = pyautogui.position()
print(f"  X: {x}, Y: {y}")

print("\nNow, move your mouse to the password field and press Enter...")
input("\nPress Enter when ready...")

x2, y2 = pyautogui.position()
print(f"  X: {x2}, Y: {y2}")

print("\nNow, move your mouse to the login button and press Enter...")
input("\nPress Enter when ready...")

x3, y3 = pyautogui.position()
print(f"  X: {x3}, Y: {y3}")

print("\nNow I will login using these coordinates...")
print(f"Username field: ({x}, {y})")
print(f"Password field: ({x2}, {y2})")
print(f"Login button: ({x3}, {y3})")

input("\nPress Enter to start login...")

# Click username field
print("\nClicking username field...")
pyautogui.click(x, y)
time.sleep(0.5)

# Type username
print(f"Typing username: {USERNAME}")
pyautogui.write(USERNAME)
time.sleep(0.5)

# Click password field
print("Clicking password field...")
pyautogui.click(x2, y2)
time.sleep(0.5)

# Type password
print("Typing password...")
pyautogui.write(PASSWORD)
time.sleep(0.5)

# Click login button
print("Clicking login button...")
pyautogui.click(x3, y3)

print("\n[OK] Login clicked!")
print("Wait 5 seconds to check if login was successful...")

time.sleep(5)

print("\nTest completed!")
print("If login was successful, you should be logged in to chess.com")