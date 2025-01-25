
# import json
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import re
# from Amount_Of_Data import namesAndCount
# from ScrollToLoadAllVideos import scroller
# from ViewCount import convert_views, convert_date
# import numpy as np
# from selenium.webdriver.chrome.options import Options
# from timeConvert import duration_to_seconds
# from DriverOpen import driverOpenFunc
# def scraper(channel_url,j):
#     # Get the video names and the number of videos
#     video_names, n = namesAndCount(channel_url)

#     metadata = {"videos": []}
#     left = 0
#     right = 20

#     # Initialize WebDriver with ChromeDriver and Brave options
#     driver = driverOpenFunc()
#     driver.switch_to.window(driver.window_handles[0])

#     while right < n:
#         # Open the channel
#         driver.get(channel_url)
#         # driver.fullscreen_window()
#         time.sleep(5)

#         # Scroll to the bottom
#         scroller(driver)

#         # All video elements
#         video_elements = driver.find_elements(By.ID, 'video-title')
        

#         for i in range(left, right):
#             if i > 0 and i % 30 == 0:
#                 scroller(driver)

#             try:
#                 video_elements = driver.find_elements(By.ID, 'video-title')
#                 driver.execute_script("arguments[0].scrollIntoView(true);", video_elements[i])
#                 time.sleep(1)
#                 driver.execute_script("arguments[0].click();", video_elements[i])
#                 time.sleep(3)

#                 # Fetch metadata element and extract its text
#                 container = driver.find_element(By.ID, "info-container")
#                 driver.execute_script("arguments[0].click();", container)


#                 meta_text_str = str(container.text)
#                 print(meta_text_str)
#                 meta_text_str=meta_text_str.split(" ")
                
#                 # Use regex to extract views, date, and products from the metadata text
#                 # views = re.search(r'([\d,]+[KMB]?)\s+views', meta_text_str)
#                 # date = re.search(r'(\d{1,2}\s\w+\s\d{4})', meta_text_str)
#                 # products = re.search(r'(\d+)\s+products', meta_text_str)
#                 duration = driver.find_element(By.CLASS_NAME,"ytp-time-duration")
#                 views = meta_text_str[0]
#                 date = meta_text_str[2:5]
#                 products = meta_text_str[6]

#                 # Clean up extracted data
#                 # cleaned_views = convert_views(views.group(1).replace(",", "")) if views else np.nan
#                 # cleaned_date = convert_date(date.group(1)) if date else np.nan
#                 # cleaned_products = products.group(1) if products else np.nan
#                 # duration = duration.text
                
#                 # Store the extracted data in the dictionary
#                 video_data = {
#                     "video title": video_names[i],
#                     "views": str(views),
#                     "days ago": ' '.join(date),
#                     "products": products,
#                     "duration": duration_to_seconds(duration)
#                 }
#                 metadata['videos'].append(video_data)

#                 print(f"Video {i}: {video_data}")  # Output the metadata for this video
#                 with open(f'checker{j}.json', 'w') as json_file:
#                     json.dump(metadata, json_file, indent=4)

#                 # Navigate back to the video list
#                 driver.back()
#                 time.sleep(3)  # Wait for the page to load after going back

#             except Exception as e:
#                 print(f"An error occurred at video {i}: {e}")
#                 try:
#                     driver.back()  # Ensure we go back even if an error occurs
#                     time.sleep(3)  # Wait for the page to load after going back
#                 except Exception as back_error:
#                     print(f"Error navigating back: {back_error}")

#         left += 20
#         right += 20

#     # Write all metadata to the JSON file at once
#     with open(f'metadata{j}.json', 'w') as json_file:
#         json.dump(metadata, json_file, indent=4)

#     driver.quit()  # Close the WebDriver
#     return metadata

# scraper("https://www.youtube.com/@kurzgesagt/videos",1)




import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from Amount_Of_Data import namesAndCount
from ScrollToLoadAllVideos import scroller
from ViewCount import convert_views, convert_date
import numpy as np
from selenium.webdriver.chrome.options import Options
from timeConvert import duration_to_seconds
from DriverOpen import driverOpenFunc

def scroller(driver):
    """Scrolls the page to load all videos."""
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scraper(channel_url, j):
    # Get the video names and the number of videos
    video_names, n = namesAndCount(channel_url)

    metadata = {"videos": []}
    left = 0
    right = 20

    # Initialize WebDriver with ChromeDriver and Brave options
    driver = driverOpenFunc()
    driver.switch_to.window(driver.window_handles[0])

    while right < n:
        # Open the channel
        driver.get(channel_url)
        time.sleep(5)

        # Scroll to the bottom
        scroller(driver)

        # All video elements
        video_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, 'video-title'))
        )

        for i in range(left, right):
            if i > 0 and i % 30 == 0:
                scroller(driver)

            try:
                video_elements = driver.find_elements(By.ID, 'video-title')
                driver.execute_script("arguments[0].scrollIntoView(true);", video_elements[i])
                time.sleep(1)
                driver.execute_script("arguments[0].click();", video_elements[i])
                time.sleep(3)

                # Fetch metadata element and extract its text
                container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "info-container"))
                )
                driver.execute_script("arguments[0].click();", container)

                meta_text_str = container.text
                print(meta_text_str)
                
                # Extract views, date, and products using regex
                views = re.search(r'([\d,]+)\sviews', meta_text_str)
                date = re.search(r'(\w+\s\d{1,2},\s\d{4})', meta_text_str)
                products = re.search(r'(\d+)\sproducts', meta_text_str)
                duration = driver.find_element(By.CLASS_NAME, "ytp-time-duration").text

                # Clean up extracted data
                cleaned_views = views.group(1) if views else "0"
                cleaned_date = date.group(1) if date else "Unknown Date"
                cleaned_products = products.group(1) if products else "0"
                duration_seconds = duration_to_seconds(duration)

                # Store the extracted data in the dictionary
                video_data = {
                    "video title": video_names[i],
                    "views": cleaned_views,
                    "days ago": cleaned_date,
                    "products": cleaned_products,
                    "duration": duration_seconds
                }
                metadata['videos'].append(video_data)

                print(f"Video {i}: {video_data}")  # Output the metadata for this video
                with open(f'checker{j}.json', 'w') as json_file:
                    json.dump(metadata, json_file, indent=4)

                # Navigate back to the video list
                driver.back()
                time.sleep(3)  # Wait for the page to load after going back

            except Exception as e:
                print(f"An error occurred at video {i}: {e}")
                try:
                    driver.back()  # Ensure we go back even if an error occurs
                    time.sleep(3)  # Wait for the page to load after going back
                except Exception as back_error:
                    print(f"Error navigating back: {back_error}")

        left += 20
        right += 20

    # Write all metadata to the JSON file at once
    with open(f'metadata{j}.json', 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

    driver.quit()  # Close the WebDriver
    return metadata

# Example usage
scraper("https://www.youtube.com/@kurzgesagt/videos", 1)
