from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
def driverOpenFunc():
    chrome_options = Options()
    adblock_extension_path = r"D:\YouTube-Likes-predictor\adblock.crx"  # Ensure this path is correct
    chrome_options.add_extension(adblock_extension_path)
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")

    # Initialize WebDriver with ChromeDriver and options
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(2)
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[1])  # Switch to the second tab
        driver.close()  # Close the tab
        driver.switch_to.window(driver.window_handles[0])  # Switch back to the main tab
    
    return driver
