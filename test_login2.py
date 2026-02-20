"""
Test login script - with modal closing
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

    # Close cookie banner
    try:
        cookie_accept = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Accept cookies']")
        cookie_accept.click()
        print("Closed cookie banner")
        time.sleep(1)
    except:
        print("No cookie banner found")

    # Close any modal with close button
    try:
        close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Close']")
        if close_buttons:
            for btn in close_buttons:
                try:
                    btn.click()
                    print("Closed modal")
                    time.sleep(1)
                except:
                    pass
    except:
        print("No modals found")

    # Take screenshot before interacting
    driver.save_screenshot("test2_before_interact.png")
    print("Screenshot saved: test2_before_interact.png")

    # Find username field - wait longer
    username_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    print(f"Found username field")

    # Scroll to element
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_field)
    time.sleep(1)

    # Wait for element to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of(username_field)
    )

    # Click on username field first
    username_field.click()
    time.sleep(0.5)

    # Clear and enter username
    username_field.clear()
    username_field.send_keys(username)
    print(f"Entered username: {username}")

    time.sleep(0.5)

    # Find password field - wait longer
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password"))
    )

    print(f"Found password field")

    # Scroll to element
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_field)
    time.sleep(1)

    # Wait for element to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of(password_field)
    )

    # Click on password field first
    password_field.click()
    time.sleep(0.5)

    # Clear field
    password_field.clear()
    time.sleep(0.3)

    # Enter password
    password_field.send_keys(password)
    print("Entered password")

    # Take screenshot after filling
    driver.save_screenshot("test2_after_fill.png")
    print("Screenshot saved: test2_after_fill.png")

    time.sleep(2)

    # Find and click login button - wait longer
    login_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login"))
    )

    # Scroll to button
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_button)
    time.sleep(1)

    # Wait for button to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(login_button)
    )

    # Click using JavaScript
    driver.execute_script("arguments[0].click();", login_button)
    print("Clicked login button")

    # Wait for redirect
    time.sleep(5)

    # Check if login successful
    if "chess.com/login" not in driver.current_url:
        print("✅ Login successful!")
        print(f"Current URL: {driver.current_url}")
        driver.save_screenshot("test2_success.png")
    else:
        print("❌ Login failed!")
        driver.save_screenshot("test2_failed.png")

    time.sleep(10)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    driver.save_screenshot("test2_error.png")
    print("Screenshot saved: test2_error.png")

finally:
    driver.quit()
    print("Browser closed")