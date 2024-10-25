import time
from selenium import webdriver
from threading import Thread
from Scraper import scraper

# URLs to scrape
first_url = "https://www.youtube.com/@kurzgesagt/videos"
second_url = "https://www.youtube.com/@statquest/videos"

# Create threads for simultaneous scraping
thread1 = Thread(target=scraper, args=(first_url,))
thread2 = Thread(target=scraper, args=(second_url,))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

print("Both scraping tasks completed!")
