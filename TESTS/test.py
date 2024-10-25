import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import re
try:

    # Initialize WebDriver and open the YouTube channel in headless mode
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/watch?v=VD6xJq8NguY&pp=ygUVa3VyZ2FzdCBpbiBhIG51dHNoZWxs")

    # Let the page load
    time.sleep(5)

    print("Page opened successfully")

    # Fetch metadata element and extract its text
    container = driver.find_element(By.ID, "info-container")
    driver.execute_script("arguments[0].click();", container)
    print(container.text)
    meta_text_str=container.text

    time.sleep(500)
    views = re.search(r'([\d,]+)', meta_text_str)  # Extracts "3954890" (views without "views")
    # date = re.search(r'(\d{1,2} \w+ \d{4})', meta_text_str)  # Extracts date as "3 Oct 2024"
    date= driver.find_element(By.ID,"date-text").text
    products = re.search(r'(\d+)(?= products)', meta_text_str)  # Extracts the number of products "7"
    cleaned_views = views.group(1).replace(",", "") if views else "N/A"
    
    likes=driver.find_element(By.CLASS_NAME,"yt-spec-button-shape-next__button-text-content")
    
    print(date,products,cleaned_views,likes.text)


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Always close the driver session at the end
    driver.quit()
