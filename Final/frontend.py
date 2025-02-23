import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import string
import json
from Scraper import scraper
st.header("Youtube data Scraper")
url = st.text_area("Enter the URL")
name = url[25:-7]
wait_time = st.number_input("Enter Delay Duration in seconds", 1)
if st.button("Press To start"):
    st.html(f"<p>{name} videos metadata<p>")
    scraper(url, name = name, continuous=True, interval=wait_time)
    uploaded_file = st.file_uploader(f"{name}.json", type=["json"])
