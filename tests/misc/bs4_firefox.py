import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

def render_page(url):
    driver = webdriver.Firefox()
    driver.get(url)
    r = driver.page_source
    #driver.quit()
    return r

query = "define:lucid"
goog_search = "https://www.google.co.uk/search?q=" + query

r = render_page(goog_search)

soup = BeautifulSoup(r, "html.parser")
print(soup.prettify())