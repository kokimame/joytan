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


def get_def_content(word):
    r = requests.get(url_dict + word + "?s=t")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    defcs = soup.find_all(attrs={"class":"def-content"}) # Def-contents
    defcs = [re.sub('\<.*\>', '', defc.text.strip()) for defc in defcs]
    return defcs



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
    
    def get_script(self, num=""):
        script = "Word %s: %s\n" % (num, word)
        for n, content in enumerate(self.contents):
            script += "%d. %s.\n"  % (n+1, content['Define'])
            if content['Example'] != False:
                script += "Ex. %s\n" % content['Example']
            else:
                script += "\n"
        return script


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

#list_word_content(words[53:69])

scriptname = "script101"
ftype = ".txt"
atype = ".aiff"


call(["rm", scriptname + ftype])
for i, word in enumerate(words[0:30]):
    wc = get_word_content(word)
    scr = wc.get_script(num="%d" % (i+1))
    print(scr)

    with open(scriptname + ftype, "a") as script:
        script.write(scr)
    time.sleep(1.0)

call(["say", "-f", scriptname + ftype , "-o", scriptname + atype])
call(["lame", "-m", "m", scriptname+atype, scriptname+".mp3"])
call(["afplay", scriptname+".mp3"])
#list_words(words[0:3])
#list_words(words[99:102])
