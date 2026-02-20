"""
Test Chrome profile without headless
"""

import time
import undetected_chromedriver as uc

# Config
user_data_dir = r"C:\Users\dhuy8\.openclaw\AppData\Local\Google\Chrome\User Data"
profile_directory = "Default"

print("="*60)
print("TEST CHROME PROFILE (NO HEADLESS)")
print("="*60)
print(f"User Data Dir: {user_data_dir}")
print(f"Profile: {profile_directory}")
print()

# Setup options
options = uc.ChromeOptions()

# Add user-data-dir
options.add_argument(f'--user-data-dir={user_data_dir}')
options.add_argument(f'--profile-directory={profile_directory}')

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
        print("[INFO] Not logged in")

    print("Waiting 10 seconds before closing...")
    time.sleep(10)

    driver.quit()
    print("[OK] Driver closed")

    print("\n[SUCCESS] Test completed!")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()