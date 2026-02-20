"""
Test PyAutoGUI click
"""

import pyautogui
import time

print("Testing PyAutoGUI...")

# Move mouse to center of screen
screen_width, screen_height = pyautogui.size()
center_x = screen_width // 2
center_y = screen_height // 2

print(f"Screen size: {screen_width}x{screen_height}")
print(f"Center: ({center_x}, {center_y})")

print("\nMoving mouse to center...")
pyautogui.moveTo(center_x, center_y, duration=1)

print(f"Current position: {pyautogui.position()}")

print("\nClicking...")
pyautogui.click()

print("\nTest completed!")