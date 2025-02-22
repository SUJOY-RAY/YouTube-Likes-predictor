# # Define a function for scraping a given URL
# import webbrowser
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# import time
# from DriverOpen import driverOpenFunc
# def namesAndCount(url):
#     driver=driverOpenFunc()
#     driver.get(url)

#     time.sleep(5)

#     scroll_pause_time = 1

#     last_height = driver.execute_script("return document.documentElement.scrollHeight")
#     video_names=[]

#     while True:
#         driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#         time.sleep(scroll_pause_time)
#         new_height = driver.execute_script("return document.documentElement.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
#     video_elements=driver.find_elements(By.ID,'video-title')
#     for a in video_elements:
#         video_names.append(a.text)
#     return video_names,len(video_names)


# # a,b=namesAndCount("https://www.youtube.com/@kurzgesagt/videos")


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from DriverOpen import driverOpenFunc
from ScrollToLoadAllVideos import scroller
def namesAndCount(url):
    driver = driverOpenFunc()
    driver.get(url)
    
    time.sleep(5)  # Wait for initial page load

    # scroll_pause_time = 1
    # last_height = driver.execute_script("return document.documentElement.scrollHeight")


    # while True:
    #     driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    #     time.sleep(scroll_pause_time)
    #     new_height = driver.execute_script("return document.documentElement.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    scroller(driver = driver)
    video_titles = []
    video_durations = []
    # Extract video titles
    video_elements = driver.find_elements(By.ID, "video-title")
    
    for video in video_elements:
        title = video.text

        if title:
            video_titles.append(title)

        # Remove element from DOM to free memory
        driver.execute_script("arguments[0].remove();", video)

    driver.quit()  # Close the browser to free resources
    return video_titles, len(video_titles)


# # Example Usage
# titles, count = namesAndCount("https://www.youtube.com/@kurzgesagt/videos")

# # Print Results
# print(f"Total Videos Scraped: {count}")
# for i in range(min(5, count)):  # Print first 5 for preview
#     print(f"{i+1}. {titles[i]}")
