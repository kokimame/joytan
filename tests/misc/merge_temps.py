import os
import re
import time
import requests

from subprocess import call
from bs4 import BeautifulSoup

import platform
if platform.system() == "Linux":
    TTS, TTS_ARG = "espeak", ["-s 150"]
elif platform.system() == "Darwin":
    TTS, TTS_ARG = "say", [""]

TOTAL_DEFS = 3

URL_WORDS = "https://crunchprep.com/gre/2014/101-high-frequency-gre-words"
URL_GSTA = "http://ssl.gstatic.com/dictionary/static/sounds/oxford/"
URL_DICT = "http://dictionary.reference.com/browse/"
GB_1 = "--_gb_1.mp3"        # A trailing type for gstatic dictionary
GB_18 = "--_gb_1.8.mp3"     # A trailing type for gstatic dictionary

TEMP_DIR = "./TEMPLATE/"
TEST_DIR = "./test_mp3/"
MERGE_DIR = "./merged/"
MP3 = ".mp3"

def get_mp3(word, dir=""):
    for w_key in [word + GB_1, word + GB_18, "x" + word + GB_18]:
        r = requests.get(URL_GSTA + w_key, stream=True)
        if r.ok:
            break
        elif w_key == "x" + word and not r.ok:
            raise Exception("Audio for '" + word + "' not found")
    filename = dir + word + ".mp3"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(r.content)

def merge_mp3(input1, input2, output):
    cmd = "cat %s %s > %s" % (input1, input2, output)
    call(cmd, shell=True)

def word_header(dir, word, read=3):
    w_path = dir + word + ".mp3"
    if read < 1: raise Exception("Error: Read a word at least once (read >= 1)")
    cmd = ""
    for i in range(1, read+1):
        cmd += "%s " % w_path

    cmd = "cat " + TEMP_DIR + "word.mp3 " + cmd + " > w_" + word + "%d.mp3" % read
    call(cmd, shell=True)


word_header(TEST_DIR, "laconic")

#merge_mp3(TEST_DIR + "laconic.mp3", TEST_DIR + "laconic.mp3", "laconic2.mp3")
#merge_mp3("laconic2.mp3", TEST_DIR + "laconic.mp3", "laconic3.mp3")
#merge_mp3(TEMP_DIR + "word.mp3", "laconic3.mp3", "w_laconic3.mp3")