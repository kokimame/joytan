import requests
from bs4 import BeautifulSoup

url = "www.pythonforbeginners.com"

r = requests.get("http://" + url)
data = r.text

soup = BeautifulSoup(data)

for link in soup.find_all("a"):
    print(link.get("href"))