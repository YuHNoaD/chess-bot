"""
Test Chrome profile
"""

import time
import undetected_chromedriver as uc

# Config
user_data_dir = r"C:\Users\dhuy8\AppData\Local\Google\Chrome\User Data"
profile_directory = "Default"

print("="*60)
print("TEST CHROME PROFILE")
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
options.add_argument('--disable-infobars')

print("Creating Chrome driver...")

try:
    driver = uc.Chrome(options=options, version_main=144)
    print("[OK] Chrome driver created successfully")

    # Go to chess.com
    print("Going to chess.com...")
    driver.get("https://www.chess.com")

    # Wait
    time.sleep(5)

    # Check if logged in
    print("Checking login status...")

    # Look for user menu
    try:
        user_menu = driver.find_elements("css selector", "[data-cy='user-menu']")
        username_element = driver.find_elements("css selector", "[data-cy='user-username']")

        if user_menu or username_element:
            print("[OK] Already logged in!")
            print("[INFO] Chrome profile is working correctly")
        else:
            print("[INFO] Not logged in - profile might not have cookies")
    except Exception as e:
        print(f"[ERROR] Cannot check login status: {e}")

    # Take screenshot
    driver.save_screenshot("test_chrome_profile.png")
    print("[INFO] Screenshot saved: test_chrome_profile.png")

    # Wait
    time.sleep(5)

    # Close
    driver.quit()
    print("[OK] Driver closed")

    print("\n" + "="*60)
    print("TEST COMPLETED")
    print("="*60)

except Exception as e:
    print(f"[ERROR] Test failed: {e}")
    import traceback
    traceback.print_exc()