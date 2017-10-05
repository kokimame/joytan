import os
import re
import requests
from subprocess import call
from bs4 import BeautifulSoup

def get_mp3(word):
    for w_key in [word + gb_1, word + gb_18, "x" + word + gb_18]:
        r = requests.get(url_mp3 + w_key, stream=True)
        if r.ok:
            break
        elif w_key == "x" + word and not r.ok:
            raise Exception("Audio for '" + word + "' not found")


def get_meaning(word):
    r = requests.get(url_dict + word + "?s=t")
    data = r.text
    print(data)
    items = re.findall('<meta name="description" content="'+".*$", data, re.MULTILINE)
    for x in items:
        y = x.replace('<meta name="description" content="', '')
        z = y.replace(' See more."/>', '')
        m = re.findall('at Dictionary.com, a free online dictionary with pronunciation,' +
                       '              synonyms and translation. Look it up now! "/>',z)

        if m == []:
            if z.startswith("Get your reference question answered by Ask.com"):
                print("Word not found! :(")
            else:
                print(z)
        else:
            print("Word not found! :(")

def get_meaning2(word):
    r = requests.get(url_dict + word + "?s=t")
    data = r.text
    #print(data)
    soup = BeautifulSoup(data, "html.parser")
    desc = soup.find_all(attrs={"name":"description"})
    #print(descript)
    return desc[0]['content']


url_words = "https://crunchprep.com/gre/2014/101-high-frequency-gre-words"
url_mp3 = "http://ssl.gstatic.com/dictionary/static/sounds/oxford/"
url_dict = "http://dictionary.reference.com/browse/"

gb_1 = "--_gb_1.mp3"
gb_18 = "--_gb_1.8.mp3"

r = requests.get(url_words)
data = r.text

soup = BeautifulSoup(data, "html.parser")
words = soup.find_all("strong")
words = [word.text.lower() for word in words[1:102]]

a_desc = get_meaning2("laconic")
b_desc = get_meaning2("effete")

call(["say", b_desc])

