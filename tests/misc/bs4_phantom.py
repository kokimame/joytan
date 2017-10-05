"""
PhantomJS doesn't contain audio elements on the front page
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def open_page(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    r = driver.page_source
    return r

query = "define:lucid"
goog_search = "https://www.google.co.uk/search?q=" + query

r = open_page(goog_search)

soup = BeautifulSoup(r, "html.parser")
print(soup.prettify())