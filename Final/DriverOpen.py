from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def driverOpenFunc():
    chrome_options = Options()
    
    # Set the path to Brave Browser
    # brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    # chrome_options.binary_location = brave_path  # Point Selenium to Brave
    
    # Common options for stability
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")  # Fullscreen mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging
    chrome_options.add_argument("--headless")
    
    # Optional: Enable ad-blocker extension
    # ad_block = "D:/YouTube-Likes-predictor/adblock.crx"
    # chrome_options.add_extension(ad_block)
    
    # Set the path to Chromedriver
    chromedriver_path = "D:/YouTube-Likes-predictor/chromedriver.exe"
    s = Service(chromedriver_path)

    # Initialize Brave WebDriver
    driver = webdriver.Chrome(service=s, options=chrome_options)
    
    return driver
