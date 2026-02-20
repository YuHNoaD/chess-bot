"""
Test login script
"""

import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
username = "YuHNoaD"
password = "YuHNoaD06@"

# Setup driver
options = uc.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_argument('--no-first-run')
options.add_argument('--no-default-browser-check')

driver = uc.Chrome(options=options, version_main=144)

try:
    # Go to login page
    driver.get("https://www.chess.com/login")
    time.sleep(5)

    print("Page loaded")

    # Find username field
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    print(f"Found username field: {username_field}")

    # Enter username
    username_field.clear()
    username_field.send_keys(username)
    print(f"Entered username: {username}")

    # Find password field
    password_field = driver.find_element(By.ID, "password")

    print(f"Found password field: {password_field}")

    # Click on password field first
    password_field.click()
    time.sleep(0.5)

    # Clear field
    password_field.clear()
    time.sleep(0.3)

    # Enter password character by character
    for char in password:
        password_field.send_keys(char)
        time.sleep(0.05)

    print("Entered password")

    # Take screenshot
    driver.save_screenshot("test_before_login.png")
    print("Screenshot saved: test_before_login.png")

    time.sleep(2)

    # Find and click login button
    login_button = driver.find_element(By.ID, "login")
    login_button.click()

    print("Clicked login button")

    # Wait for redirect
    time.sleep(5)

    # Check if login successful
    if "chess.com/login" not in driver.current_url:
        print("✅ Login successful!")
        print(f"Current URL: {driver.current_url}")
    else:
        print("❌ Login failed!")
        driver.save_screenshot("test_after_login.png")
        print("Screenshot saved: test_after_login.png")

    time.sleep(10)

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("test_error.png")
    print("Screenshot saved: test_error.png")

finally:
    driver.quit()
    print("Browser closed")