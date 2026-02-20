"""
Test with new profile (no user-data-dir)
"""

import time
import undetected_chromedriver as uc

print("="*60)
print("TEST WITH NEW PROFILE")
print("="*60)
print()

# Setup options
options = uc.ChromeOptions()

# Anti-detection
options.add_argument('--disable-blink-features=AutomationControlled')

print("Creating Chrome driver...")

try:
    driver = uc.Chrome(options=options, version_main=144)
    print("[OK] Chrome driver created")

    # Go to chess.com
    print("Going to chess.com...")
    driver.get("https://www.chess.com")

    print("Waiting 10 seconds...")
    time.sleep(10)

    # Check login status
    print("Checking login status...")

    # Look for user menu
    user_menu = driver.find_elements("css selector", "[data-cy='user-menu']")
    username_element = driver.find_elements("css selector", "[data-cy='user-username']")

    if user_menu or username_element:
        print("[OK] Already logged in!")
        if username_element:
            print(f"[INFO] Username: {username_element[0].text}")
    else:
        print("[INFO] Not logged in - need to login")

    print("Waiting 10 seconds before closing...")
    time.sleep(10)

    driver.quit()
    print("[OK] Driver closed")

    print("\n[SUCCESS] Test completed!")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()