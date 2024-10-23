import time
from selenium import webdriver
from threading import Thread

import Final.Amount_Of_Data as Amount_Of_Data


# URLs to scrape
first_url = "https://www.example.com"
second_url = "https://www.another-example.com"

# Create threads for simultaneous scraping
thread1 = Thread(target=scrape, args=(first_url,))
thread2 = Thread(target=scrape, args=(second_url,))

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

print("Both scraping tasks completed!")
