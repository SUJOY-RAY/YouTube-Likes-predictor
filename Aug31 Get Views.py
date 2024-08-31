import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the WebDriver (make sure you have the appropriate driver installed)
driver = webdriver.Chrome()


# Open the YouTube channel page
channel_url = "https://www.youtube.com/@kurzgesagt/videos"
driver.get(channel_url)

# Allow the page to load
time.sleep(5)

scroll_pause_time = 1

# Get the height of the entire webpage
last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # Wait for the page to load
    time.sleep(scroll_pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

video=driver.find_elements(By.ID, "metadata-line")
titles=[]
for a in video:
    titles.append(a.text)

print(titles)




