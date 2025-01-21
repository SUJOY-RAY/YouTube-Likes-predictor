
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from Amount_Of_Data import namesAndCount
from ScrollToLoadAllVideos import scroller
from ViewCount import convert_views, convert_date
import numpy as np
from selenium.webdriver.chrome.options import Options


def scraper(channel_url,j):
    # Get the video names and the number of videos
    video_names, n = namesAndCount(channel_url)

    metadata = {"videos": []}
    left = 0
    right = 20
    # brave_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application"
    chrome_options=Options()
    # chrome_options.binary_location=brave_path
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize WebDriver with ChromeDriver and Brave options
    driver = webdriver.Chrome(options=chrome_options)

    while right < n:
        # Open the channel
        driver.get(channel_url)
        time.sleep(5)

        # Scroll to the bottom
        scroller(driver)

        # All video elements
        video_elements = driver.find_elements(By.ID, 'video-title')

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
                container = driver.find_element(By.ID, "info-container")
                

                meta_text_str = container.text

                # Use regex to extract views, date, and products from the metadata text
                views = re.search(r'([\d,]+[KMB]?)\s+views', meta_text_str)
                date = re.search(r'(\d+\s+(?:hours?|days?|weeks?|months?|years?)\s+ago)', meta_text_str)
                products = re.search(r'(\d+)\s+products', meta_text_str)
                duration = driver.find_element(By.CLASS_NAME,"ytp-time-duration")


                # Clean up extracted data
                cleaned_views = convert_views(views.group(1).replace(",", "")) if views else np.nan
                cleaned_date = convert_date(date.group(1)) if date else np.nan
                cleaned_products = products.group(1) if products else np.nan
                duration = duration.text
                
                # Store the extracted data in the dictionary
                video_data = {
                    "video title": video_names[i],
                    "views": cleaned_views,
                    "days ago": cleaned_date,
                    "products": cleaned_products,
                    "duration": duration
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

scraper("https://www.youtube.com/@kurzgesagt/videos",1)
