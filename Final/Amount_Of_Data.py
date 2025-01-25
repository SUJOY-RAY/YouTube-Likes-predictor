# Define a function for scraping a given URL
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By

import time
from DriverOpen import driverOpenFunc
def namesAndCount(url):
    driver=driverOpenFunc()
    driver.get(url)

    time.sleep(5)

    scroll_pause_time = 1

    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    video_elements=driver.find_elements(By.ID,'video-title')
    video_names=[]
    for a in video_elements:
        video_names.append(a.text)
    return video_names,len(video_names)


# a,b=namesAndCount("https://www.youtube.com/@kurzgesagt/videos")
