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


def call_tts(script):
    call([TTS, script, *TTS_ARG])

TOTAL_DEFS = 3

URL_WORDS = "https://crunchprep.com/gre/2014/101-high-frequency-gre-words"
URL_GSTA = "http://ssl.gstatic.com/dictionary/static/sounds/oxford/"
URL_DICT = "http://dictionary.reference.com/browse/"
GB_1 = "--_gb_1.mp3"        # A trailing type for gstatic dictionary
GB_18 = "--_gb_1.8.mp3"     # A trailing type for gstatic dictionary

TEMP_DIR = "./TEMPLATE/"
TEST_DIR = "./test_mp3/"
MERG_DIR = "./MERGED/"
MP3 = ".mp3"

def get_mp3(word, dir="./"):
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

def packet_compile(filename, dir_packets):
    cmd = "cat %s* > %s" % (dir_packets, filename)
    call(cmd, shell=True)



def espeak_mp3(script, output):
    call(["rm", "-f", output])
    os.makedirs(os.path.dirname(output), exist_ok=True)
    cmd = 'espeak "%s" --stdout | ' \
          'ffmpeg -loglevel panic -i - -ar 44100 -ab 192k -f mp3 %s' % (script, output)
    call(cmd, shell=True)


def say_mp3(script, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    cmd = 'say "%s" -o %s.aiff;' \
          'ffmpeg -loglevel panic -i %s.aiff -acodec libmp3lame -ar 44100 -ab 192k -f mp3 %s.mp3' \
          % (script, output, output, output)
    call(cmd, shell=True)

def set_bgm(original, path2bgm):
    call("sox -m %s %s %s" % (path2bgm, original, "bgm-"+original), shell=True)


class Packet:
    def __init__(self, word, num, max=5):
        self.word = word
        self.num = num
        self.snum = (max - len(str(num))) * '0' + str(num) + "-"
        self.directory = "./" + self.word + "/"
        self.contents = []
        self.packet_seq = {0:""}

    def fetch_content(self):
        for n, defc in enumerate(self.get_def_content(self.word)):
            if n + 1 >= TOTAL_DEFS: break
            try:
                define, exam = defc.split(":")
                exam = exam.strip()
            except ValueError:
                define, exam = defc, False
            self.contents.append({'define': define, 'example': exam})

    def word_header(self, read=3, path2mp3="word.mp3"):
        if read < 1: raise Exception("Error: Read a word at least once (read >= 1)")
        get_mp3(self.word, self.directory)
        w_path = self.directory + self.word + ".mp3"
        # WARNING: Don't add '.mp3' because 'say' command creates '.aiff' internal
        n_path = self.directory + str(self.num)

        if platform.system() == "Linux":
            espeak_mp3("%s. " % str(self.num), n_path + ".mp3")
        if platform.system() == "Darwin":
            say_mp3("%s. " % str(self.num), n_path)

        cmd = "cat %s %s " % (path2mp3, n_path + ".mp3")
        for i in range(1, read+1):
            cmd += "%s " % w_path

        cmd += " > " + self.directory + self.word + "-wh.mp3"
        call(cmd, shell=True)
        self.packet_seq[max(self.packet_seq, key=int)+1] = self.directory + self.word + "-wh.mp3"


    def content_data(self, ex_sfx="", def_sfx=""):
        for n, content in enumerate(self.contents):
            fdef = self.word + "-def-%d" % (n+1)
            def_mp3 = self.directory + fdef + ".mp3"

            if platform.system() == "Linux":
                espeak_mp3("%d.\n" % (n+1) + content['define'] + "\n", def_mp3) # Save def contents as .mp3
                call("cat %s %s > %s" % (def_sfx, def_mp3, self.directory + "-sfx" + fdef + ".mp3"), shell=True) # Cat def content with sound effects
                self.packet_seq[max(self.packet_seq, key=int) + 1] = self.directory + "-sfx" + fdef + ".mp3"
                if content['example'] != False:
                    self.packet_seq[max(self.packet_seq, key=int) + 1] = ex_sfx + TEMP_DIR + "ex.mp3"
                    espeak_mp3(content['example'] + "\n", self.directory + fdef + "-ex.mp3")
                    self.packet_seq[max(self.packet_seq, key=int) + 1] = self.directory + fdef + "-ex.mp3"

            if platform.system() == "Darwin":
                say_mp3("%d. " % (n+1) + content['define'] + "\n", self.directory + fdef)
                call("cat %s %s > %s" % (def_sfx, def_mp3, self.directory + "-sfx" + fdef + ".mp3"), shell=True)
                self.packet_seq[max(self.packet_seq, key=int) + 1] = self.directory + "-sfx" + fdef + ".mp3"
                if content['example'] != False:
                    self.packet_seq[max(self.packet_seq, key=int) + 1] = ex_sfx + TEMP_DIR + "ex.mp3"
                    say_mp3(content['example'] + "\n", self.directory + fdef + "-ex")
                    self.packet_seq[max(self.packet_seq, key=int) + 1] = self.directory + fdef + "-ex.mp3"

    def merge_contents(self):
        cmd = "cat "
        for i in range(1, max(self.packet_seq, key=int)+1):
            cmd += "%s " % self.packet_seq[i]
        cmd += "> " + MERG_DIR + self.snum + self.word + ".mp3"
        print("Done - Word %d: %s" % (self.num, self.word))
        os.makedirs(os.path.dirname(MERG_DIR + self.snum + self.word + ".mp3"), exist_ok=True)
        call(cmd, shell=True)
        call(["rm", "-f", "-r", self.directory])


    def get_def_content(self, word):
        r = requests.get(URL_DICT + word + "?s=t")
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        defcs = soup.find_all(attrs={"class": "def-content"})  # Def-contents
        defcs = [re.sub('\<.*\>', '', defc.text.strip()) for defc in defcs]
        return defcs

    def print_contents(self):
        print("~ Word: ", self.word, " ~")
        for content in self.contents:
            print("Define: ", content['define'])
            if content['example'] != False:
                print("\t -- Example: ", content['example'], end="\n\n")
            else:
                print()

    def get_script(self):
        script = "\nWord %s: %s\n" % (self.num, self.word)
        for n, content in enumerate(self.contents):
            script += "%d. %s.\n" % (n + 1, content['define'])
            if content['example'] != False:
                script += "  Ex. %s\n" % content['example']
        return script


r = requests.get(URL_WORDS)
data = r.text

soup = BeautifulSoup(data, "html.parser")
words = soup.find_all("strong")
words = [word.text.lower() for word in words[1:102]]

title = "mario"
call(["rm", "-f", title + ".mp3", title + ".txt"])

start = time.time()
for n, word in enumerate(words[0:50]):
    p = Packet(word, n+1)
    p.fetch_content()
    p.word_header(path2mp3="%s %s " % (
        TEMP_DIR+"smb_sfx/smb_powerup.mp3", TEMP_DIR + "word.mp3"))
    p.content_data(ex_sfx=TEMP_DIR + "smb_sfx/smb_jump-small.mp3 ",
                   def_sfx=TEMP_DIR + "smb_sfx/smb_coin.mp3 ")
    p.merge_contents()

    with open(title + ".txt", "a") as script:
        script.write(p.get_script())
    time.sleep(0.5)

packet_compile(title + ".mp3", MERG_DIR)
set_bgm(title+".mp3", "mario_bgm-2.mp3")

print("Packet compilation, Runtime: ", time.time() - start)


call(["rm", "-r", "-f", MERG_DIR])