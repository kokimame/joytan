import os
import re
import time
import requests
from subprocess import call
from bs4 import BeautifulSoup

import platform
if platform.system() == "Linux":
    tts, tts_arg = "espeak", ["-s 150"]
elif platform.system() == "Darwin":
    tts, tts_arg = "say", [""]

TOTAL_DEFS = 3

def get_mp3(word):
    for w_key in [word + gb_1, word + gb_18, "x" + word + gb_18]:
        r = requests.get(url_mp3 + w_key, stream=True)
        if r.ok:
            break
        elif w_key == "x" + word and not r.ok:
            raise Exception("Audio for '" + word + "' not found")


def define(word):
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


def get_def_content(word):
    r = requests.get(url_dict + word + "?s=t")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    defcs = soup.find_all(attrs={"class":"def-content"}) # Def-contents
    defcs = [re.sub('\<.*\>', '', defc.text.strip()) for defc in defcs]
    return defcs


def list_words(words):
    for word in words:
        print("Word: ", word)
        call_tts(word)
        for n, defc in enumerate(get_def_content(word)):
            if n+1 >= TOTAL_DEFS: break
            try:
                mean, use = defc.split(":")
                print("%d. %s\n\t\t\"%s\"" % (n + 1, mean, use.strip()))
                read_contents(n + 1, mean, use=use)
            except ValueError:
                mean = defc
                print("%d. %s\n" % (n + 1, mean))
                read_contents(n + 1, mean)
        time.sleep(1.0)


def get_content_dictionary(word):
    c_dict = {"Word": word}
    for n, defc in enumerate(get_def_content(word)):
        if n+1 >= TOTAL_DEFS: break
        try:
            define, exam = defc.split(":")
        except ValueError:
            define, exam = defc, False
        c_dict['Define'] = define
        c_dict['Example'] = exam
    return c_dict


def list_word_content(words):
    for word in words:
        wc = get_word_content(word)
        wc.print_contents()
        time.sleep(1.4)


def get_word_content(word):
    wc = WordContent(word)
    for n, defc in enumerate(get_def_content(word)):
        if n+1 >= TOTAL_DEFS: break
        try:
            define, exam = defc.split(":")
            exam = exam.strip()
        except ValueError:
            define, exam = defc, False
        wc.set_content(define, exam)
    return wc


def call_tts(script):
    call([tts, script, *tts_arg])

def read_contents(n, mean, use=""):
    if platform.system() == "Linux":
        call_tts("%d.\n %s.\n" % (n, mean))
        if use != "":
            call_tts("Ex: %s" % use)
    if platform.system() == "Darwin":
        call_tts("%d. %s." % (n, mean))
        if use != "":
            call_tts("Ex: %s" % use)

class WordContent:
    def __init__(self, name):
        self.name = name
        self.contents = []

    def set_content(self, define, exam):
        self.contents.append({'Define' : define, 'Example' : exam})

    def print_contents(self):
        print("~ Word: ", self.name, " ~")
        for content in self.contents:
            print("Define: ", content['Define'])
            if content['Example'] != False:
                print("\t -- Example: ", content['Example'], end="\n\n")
            else:
                print()

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

list_word_content(words[53:69])

#list_words(words[0:3])
#list_words(words[99:102])
