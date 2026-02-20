"""
Minimal test for Chrome driver
"""

import undetected_chromedriver as uc

print("Creating Chrome driver...")

try:
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = uc.Chrome(options=options, version_main=144)
    print("[OK] Chrome driver created")

    driver.get("https://www.google.com")
    print(f"[OK] Page loaded: {driver.title}")

    driver.quit()
    print("[OK] Driver closed")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()