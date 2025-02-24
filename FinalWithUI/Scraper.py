# import json
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import re
# from Amount_Of_Data import namesAndCount
# from ScrollToLoadAllVideos import scroller
# from selenium.webdriver.chrome.options import Options
# from timeConvert import date_convert
# from DriverOpen import driverOpenFunc


# import time
# import json
# import re
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def scraper(channel_url, name, continuous=True, interval=3600):
#     """
#     Scrapes YouTube channel videos and continuously updates the JSON file.
    
#     Parameters:
#     - channel_url (str): The YouTube channel's videos page URL.
#     - j (int): File identifier for saving.
#     - continuous (bool): Whether to run indefinitely (default=True).
#     - interval (int): Time interval in seconds before re-scraping (default=1 hour).
#     """
    
#     json_filename = f'{name}.json'

#     # Load existing data to avoid duplicates
#     if os.path.exists(json_filename):
#         with open(json_filename, 'r') as file:
#             try:
#                 metadata = json.load(file)
#             except json.JSONDecodeError:
#                 metadata = {"videos": []}
#     else:
#         metadata = {"videos": []}

#     existing_titles = {video["video title"] for video in metadata["videos"]}

#     while True:  # Infinite loop for continuous scraping
#         print("\n🔄 Starting new scrape cycle...\n")
        
#         try:
#             video_names, n = namesAndCount(channel_url)
#             left, right = 0, 50

#             try:
#                 driver = driverOpenFunc()
#                 driver.switch_to.window(driver.window_handles[0])
#             except Exception as e:
#                 print(f"❌ Error initializing WebDriver: {e}")
#                 return None

#             while left < n:
#                 driver.get(channel_url)
#                 time.sleep(5)
#                 scroller(driver)

#                 try:
#                     video_elements = WebDriverWait(driver, 10).until(
#                         EC.presence_of_all_elements_located((By.ID, 'video-title'))
#                     )
#                 except Exception as e:
#                     print(f"⚠️ Error loading video elements: {e}")
#                     break

#                 for i in range(left, min(right, n)):
#                     if i >= len(video_elements):
#                         print(f"⚠️ Skipping video {i}: Not enough video elements found.")
#                         break  

#                     if video_names[i] in existing_titles:
#                         print(f"✅ Skipping already scraped video: {video_names[i]}")
#                         continue

#                     try:
#                         video_elements = driver.find_elements(By.ID, 'video-title')
#                         driver.execute_script("arguments[0].scrollIntoView(true);", video_elements[i])
#                         time.sleep(1)
#                         driver.execute_script("arguments[0].click();", video_elements[i])
#                         time.sleep(3)
                        

#                         try:
#                             container = WebDriverWait(driver, 10).until(
#                                 EC.presence_of_element_located((By.ID, "info-container"))
#                             )
#                             driver.execute_script("arguments[0].click();", container)
#                             driver.implicitly_wait(4)
#                             container = WebDriverWait(driver, 10).until(
#                                 EC.presence_of_element_located((By.ID, "info-container"))
#                             )
#                             meta_text_str = container.text
#                             likes = driver.find_element(By.CLASS_NAME, "ytLikeButtonViewModelHost")
#                         except Exception as e:
#                             print(f"⚠️ Failed to fetch metadata for video {i}: {e}")
#                             driver.back()
#                             continue

#                         views = re.search(r'([\d,]+)\sviews', meta_text_str)
#                         date = re.search(r'(\w+\s\d{1,2},\s\d{4})', meta_text_str)
#                         products = re.search(r'(\d+)\sproducts', meta_text_str)
                        

#                         cleaned_views = views.group(1) if views else "0"
#                         cleaned_date = date.group(1) if date else "Unknown Date"
#                         cleaned_date = date_convert(cleaned_date)  
#                         cleaned_products = products.group(1) if products else "0"
#                         like_count = likes.text

#                         video_data = {
#                             "video title": video_names[i],
#                             "views": cleaned_views,
#                             "days ago": cleaned_date,
#                             "products": cleaned_products,
#                             "likes": like_count
#                         }
#                         metadata['videos'].append(video_data)
#                         existing_titles.add(video_names[i])

#                         print(f"🆕 Added: {video_data}")

#                         # Save after each video to avoid data loss
#                         with open(json_filename, 'w') as json_file:
#                             json.dump(metadata, json_file, indent=4)

#                         driver.back()
#                         time.sleep(3)

#                     except Exception as e:
#                         print(f"⚠️ Error at video {i}: {e}")
#                         try:
#                             driver.back()
#                             time.sleep(3)
#                         except Exception as back_error:
#                             print(f"⚠️ Error navigating back: {back_error}")

#                 left += 20
#                 right += 20

#             driver.quit()  

#         except Exception as main_error:
#             print(f"❌ Unexpected error: {main_error}")

#         print(f"✅ Scraping cycle complete! Next cycle in {interval//60} minutes...\n")

#         if not continuous:
#             break  # Stop if not running in continuous mode

#         time.sleep(interval)  # Wait before scraping again

# # Example usage (runs continuously, updates every interval):
# # scraper("https://www.youtube.com/@ApnaCollegeOfficial/videos", "apnacollege", continuous=True, interval=10)




import json
import os
import time
import re
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Amount_Of_Data import namesAndCount
from ScrollToLoadAllVideos import scroller
from timeConvert import date_convert
from DriverOpen import driverOpenFunc

def scraper(channel_url, name, continuous=True, interval=3600, max_retries=3):
    """
    Scrapes YouTube channel videos and continuously updates the JSON file.

    Parameters:
    - channel_url (str): The YouTube channel's videos page URL.
    - name (str): Filename identifier for saving JSON.
    - continuous (bool): Whether to run indefinitely (default=True).
    - interval (int): Time interval in seconds before re-scraping (default=1 hour).
    - max_retries (int): Maximum number of retries in case of failure.
    """
    
    json_filename = f'{name}.json'
    
    # Load existing data
    if os.path.exists(json_filename):
        try:
            with open(json_filename, 'r') as file:
                metadata = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            metadata = {"videos": []}
    else:
        metadata = {"videos": []}

    existing_titles = {video["video title"] for video in metadata["videos"]}

    while True:
        print("\n🔄 Starting new scrape cycle...\n")
        
        for attempt in range(1, max_retries + 1):
            try:
                video_names, n = namesAndCount(channel_url)
                break  # Exit retry loop if successful
            except Exception as e:
                print(f"❌ Error retrieving video count (Attempt {attempt}/{max_retries}): {e}")
                if attempt == max_retries:
                    return
                time.sleep(5)

        try:
            driver = driverOpenFunc()
            driver.switch_to.window(driver.window_handles[0])
        except WebDriverException as e:
            print(f"❌ Error initializing WebDriver: {e}")
            return

        try:
            left, right = 0, 50

            while left < n:
                driver.get(channel_url)
                time.sleep(5)

                try:
                    scroller(driver)
                    video_elements = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.ID, 'video-title'))
                    )
                except TimeoutException:
                    print("⚠️ Timeout while loading video elements. Retrying next cycle...")
                    break

                for i in range(left, min(right, n)):
                    if i >= len(video_elements):
                        print(f"⚠️ Skipping video {i}: Not enough video elements found.")
                        break  

                    if video_names[i] in existing_titles:
                        print(f"✅ Skipping already scraped video: {video_names[i]}")
                        continue

                    try:
                        video_elements = driver.find_elements(By.ID, 'video-title')
                        driver.execute_script("arguments[0].scrollIntoView(true);", video_elements[i])
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", video_elements[i])
                        time.sleep(3)

                        try:
                            container = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.ID, "info-container"))
                            )
                            driver.execute_script("arguments[0].click();", container)
                            driver.implicitly_wait(4)
                            meta_text_str = container.text
                            likes = driver.find_element(By.CLASS_NAME, "ytLikeButtonViewModelHost")
                        except (TimeoutException, NoSuchElementException) as e:
                            print(f"⚠️ Failed to fetch metadata for video {i}: {e}")
                            driver.back()
                            continue

                        views = re.search(r'([\d,]+)\sviews', meta_text_str)
                        date = re.search(r'(\w+\s\d{1,2},\s\d{4})', meta_text_str)
                        products = re.search(r'(\d+)\sproducts', meta_text_str)

                        cleaned_views = views.group(1) if views else "0"
                        cleaned_date = date.group(1) if date else "Unknown Date"
                        cleaned_date = date_convert(cleaned_date)  
                        cleaned_products = products.group(1) if products else "0"
                        like_count = likes.text if likes else "0"

                        video_data = {
                            "video title": video_names[i],
                            "views": cleaned_views,
                            "days ago": cleaned_date,
                            "products": cleaned_products,
                            "likes": like_count
                        }
                        metadata['videos'].append(video_data)
                        existing_titles.add(video_names[i])

                        print(f"🆕 Added: {video_data}")

                        # Save after each video to avoid data loss
                        with open(json_filename, 'w') as json_file:
                            json.dump(metadata, json_file, indent=4)

                        driver.back()
                        time.sleep(3)

                    except WebDriverException as e:
                        print(f"⚠️ Selenium error at video {i}: {e}")
                        try:
                            driver.back()
                            time.sleep(3)
                        except WebDriverException as back_error:
                            print(f"⚠️ Error navigating back: {back_error}")

                left += 20
                right += 20

        except Exception as main_error:
            print(f"❌ Unexpected error during scraping: {main_error}")

        finally:
            # Ensure the driver is properly closed
            try:
                driver.quit()
            except WebDriverException:
                print("⚠️ Error closing WebDriver.")

        print(f"✅ Scraping cycle complete! Next cycle in {interval//60} minutes...\n")

        if not continuous:
            break  # Stop if not running in continuous mode

        time.sleep(interval)  # Wait before scraping again



scraper("https://www.youtube.com/@kurzgesagt/videos", "kzg", continuous=True, interval=10)

