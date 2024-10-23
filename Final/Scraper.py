# import json
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time
# import re

# from Amount_Of_Data import namesAndCount
# from ScrollToLoadAllVideos import scroller


# def scraper(channel_url):
#     #Get the video names and the numebr of videos
#     video_names,n=namesAndCount(channel_url)
    
#     metadata = {"videos": []}
    
#     left=0
#     right=20

#     driver=webdriver.Chrome()

#     while(right<n):
#         #open the channel
#         driver.get(channel_url)
#         time.sleep(5)
        
#         # Scroll to the bottom
#         scroller(driver)

#         # All video elements
#         video_elements = driver.find_elements(By.ID,'video-title')

#         for i in range(left,right):
#             if i>0 and i%30==0:
#                 scroller(driver)
#             try:
#                 video_elements=driver.find_elements(By.ID,'video-title')

#                 driver.execute_script("arguments[0].scrollIntoView(true);", video_elements[i])
#                 time.sleep(1)
#                 driver.execute_script("arguments[0].click();",video_elements[i])
#                 time.sleep(3)
                
#                 # Fetch metadata element and extract its text
#                 container = driver.find_element(By.ID, "info-container")
#                 driver.execute_script("arguments[0].click();", container)
#                 print(video_elements[i],container.text)
#                 meta_text_str=container.text

#                 time.sleep(500)
#                 views = re.search(r'([\d,]+)', meta_text_str)  # Extracts "3954890" (views without "views")
#                 # date = re.search(r'(\d{1,2} \w+ \d{4})', meta_text_str)  # Extracts date as "3 Oct 2024"
#                 date= driver.find_element(By.ID,"date-text").text
#                 products = re.search(r'(\d+)(?= products)', meta_text_str)  # Extracts the number of products "7"
#                 cleaned_views = views.group(1).replace(",", "") if views else "N/A"


#                 # Store the extracted data in the dictionary
#                 video_data = {
#                     "video title": video_names[i],
#                     "views": cleaned_views if views else "N/A",
#                     "date": date.group(1) if date else "N/A",
#                     "products": products.group(1) if products else "N/A"
#                 }
#                 metadata['videos'].append(video_data)
#                 with open('metadata.json', 'a') as json_file:
#                     json.dump(metadata, json_file, indent=4)

#                 print(i)  # Output the metadata for this video
#                 driver.back()
#                 time.sleep(3)
#             except Exception as e:
#                 print(f"An error occured at video {i}",e)
#                 driver.back()
#                 time.sleep(2)
#         left+=20
#         right+=20

#     return metadata 
    


# scraper("https://www.youtube.com/@kurzgesagt/videos")


import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from Amount_Of_Data import namesAndCount
from ScrollToLoadAllVideos import scroller
from ViewCount import convert_views,convert_date

def scraper(channel_url):
    # Get the video names and the number of videos
    video_names, n = namesAndCount(channel_url)

    metadata = {"videos": []}
    left = 0
    right = 20

    driver = webdriver.Chrome()

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

                # Extract views, date, and products
                # views = re.search(r'([\d,]+) views', meta_text_str)  # Extracts views
                # date = driver.find_element(By.ID, "date-text").text  # Extracts date
                # products = re.search(r'(\d+) products', meta_text_str)  # Extracts the number of products

                # # Clean up extracted data
                # cleaned_views = views.group(1).replace(",", "") if views else "N/A"
                # cleaned_products = products.group(1) if products else "N/A"


                meta_text_str = container.text  # Extract metadata from the container
                # Use regex to extract views, date, and products from the metadata text
                print(meta_text_str)
                time.sleep(2)

                views = re.search(r'([\d,]+[KMB]?)\s+views', meta_text_str)  # Extracts views
                date = re.search(r'(\d+\s+(?:days?|weeks?|months?|years?)\s+ago)', meta_text_str)  # Extracts date
                products = re.search(r'(\d+)\s+products', meta_text_str)  # Extracts the number of products
                date = re.search(r'(\d+ (?:hours|days|weeks|months|years?) ago)', meta_text_str)  # Extracts date
                products = re.search(r'(\d+) products', meta_text_str)  # Extracts the number of products

                # Clean up extracted data
                cleaned_views = convert_views(views.group(1).replace(",", "")) if views else "N/A"
                cleaned_date = convert_date(date.group(1)) if date else "N/A"
                cleaned_products = products.group(1) if products else "N/A"




                # Store the extracted data in the dictionary
                video_data = {
                    "Video title": video_names[i],
                    "Views": cleaned_views,
                    "Days ago": cleaned_date if cleaned_date else "N/A",
                    "Products": cleaned_products
                }
                metadata['Videos'].append(video_data)

                with open('Checker.json', 'w') as json_file:
                    json.dump(metadata, json_file, indent=4)



                print(f"Video {i}: {video_data}")  # Output the metadata for this video
                
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
    with open('metadata.json', 'w') as json_file:
        json.dump(metadata, json_file, indent=4)

    driver.quit()  # Close the WebDriver
    return metadata

scraper("https://www.youtube.com/@kurzgesagt/videos")
