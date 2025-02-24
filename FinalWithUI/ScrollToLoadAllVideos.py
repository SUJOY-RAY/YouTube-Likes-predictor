import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def scroller(driver, scroll_pause_time=0.3):
    """
    Scrolls down the YouTube page to load more videos.
    
    Args:
        driver: Selenium WebDriver object used for browsing.
        scroll_pause_time: Time to pause between scrolls (default is 2 seconds).
    """
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        
        # Wait for the page to load more content
        time.sleep(scroll_pause_time)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break  # Exit the loop if no more new content is loaded
        last_height = new_height
        
# from selenium.webdriver.common.keys import Keys
# def scroller(driver, scroll_pause_time=0.3):

#     body = driver.find_element(By.TAG_NAME, "body")

#     for _ in range(80):  # Scroll 50 times
#         body.send_keys(Keys.PAGE_DOWN)
#         time.sleep(1)
