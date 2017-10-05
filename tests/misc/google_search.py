import requests
from bs4 import BeautifulSoup

research_later = "define:lucid"
goog_search = "https://www.google.co.uk/search?q=" + research_later

r = requests.get(goog_search)

soup = BeautifulSoup(r.text, "html.parser")
print(soup.prettify())