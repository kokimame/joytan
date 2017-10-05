import requests
from bs4 import BeautifulSoup

url_words = "https://crunchprep.com/gre/2014/101-high-frequency-gre-words"
r = requests.get(url_words)
data = r.text

soup = BeautifulSoup(data, "html.parser")
words = soup.find_all("strong")
words = words[1:102]

for word in words:
    print(word.text.lower())