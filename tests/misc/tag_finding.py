import urllib
from bs4 import BeautifulSoup as BS

url = '''https://archive.org/details/20070519_detroit2'''
#open and read page
page = urllib.urlopen(url)
html = page.read()
#create BeautifulSoup parse-able "soup"
soup = BS(html)
#get the src attribute from the video tag
video = soup.find("video").get("src")