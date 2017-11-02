import os, re
import requests
import subprocess
from subprocess import call, check_output
from googletrans import Translator
from gui.utils import getFileNameFromPath, mkdir, isLin, isMac, isWin

class Mp3Cmder:
    # Do NOT use OS dependent commands in this class method.
    # Those methods with the commands needs to be abstracted.
    def __init__(self, root, setting):
        self.setting = setting
        self.setting['sampling'] = 44100
        self.setting['bitrate'] = 64
        self.root = root
        self.finalDir = os.path.join(self.root, "FINAL")
        self.bgmMp3 = os.path.join(self.finalDir, "bgm.mp3")
        self.compMp3 = os.path.join(self.finalDir, "comp.mp3")
        self.finalMp3 = os.path.join(self.finalDir, "FINAL.mp3")
        self.bitkbs = None  # bit rate (Kbit/s)
        self.fskhz = None      # Sampling rate (kHz)
        self.setupAudio()
        # Dictionary to store the sequence of concatenating mp3 files for each word.
        self.catSequence = {}

        if isLin or isWin:
            self.ttscmd = espeakMp3
        elif isMac:
            self.ttscmd = sayMp3
        else:
            raise Exception("Unsurported OS found!")

        print(self.setting)

    def setupAudio(self):
        mkdir(os.path.join(self.root, "FINAL"))
        fs = self.setting['sampling']
        bps = self.setting['bitrate']

        for i, loop in enumerate(self.setting['loop']):
            if loop['sampling'] != fs:
                output = os.path.join(self.finalDir, "%s-resamp-%d.mp3" % (loop['filename'].split(".")[0], i+1))
                resampling(loop['path'], fs, output)
                loop['path'] = output
                print("%s resampled!" % loop['filename'])
            if loop['volume'] != 100:
                output = os.path.join(self.finalDir, "%s-revol-%d.mp3" % (loop['filename'].split(".")[0], i+1))
                reduceVolume(loop['path'], loop['volume'], output)
                loop['path'] = output
                print("%s volume reduced!" % loop['filename'])


        sfxGroup = self.setting['sfx']
        """ {
                'word': [{ ... items ... }, {...},
                'definition' : ...
            }
        """
        for group, sfxs in sfxGroup.items():
            sfxlist = []
            for i, sfxInfo in enumerate(sfxs):
                # Unifying sampling rate
                if sfxInfo['sampling'] != fs:
                    output = os.path.join(self.finalDir, "%s-resamp-%d.mp3" % (sfxInfo['filename'].split(".")[0], i + 1))
                    resampling(sfxInfo['path'], fs, output)
                    sfxInfo['path'] = output
                    sfxInfo['filename'] = getFileNameFromPath(output)
                    print("%s resampled!" % sfxInfo['filename'])

                # Adjusting volume by reducing it
                if sfxInfo['volume'] != 100:
                    output = os.path.join(self.finalDir, "%s-revol-%d.mp3" % (sfxInfo['filename'].split(".")[0], i + 1))
                    reduceVolume(sfxInfo['path'], sfxInfo['volume'], output)
                    sfxInfo['path'] = output
                    print("%s volume reduced!" % sfxInfo['filename'])

                # Unifying bitrate. Bitrate modification is the last otherwise causes mp3 duration bug.
                if sfxInfo['bitrate'] != bps:
                    output = os.path.join(self.finalDir, "%s-bps-%d.mp3" % (sfxInfo['filename'].split(".")[0], i + 1))
                    convertBps(sfxInfo['path'], bps, output)
                    sfxInfo['path'] = output
                    sfxInfo['filename'] = getFileNameFromPath(output)
                    print("%s bitrate modified!" % sfxInfo['filename'])
                sfxlist.append(sfxInfo['path'])
            catListMp3(sfxlist, os.path.join(self.finalDir, group + "-sfx.mp3"))



    def compileBundle(self, bw, isGstatic=True):
        curdir = os.path.join(self.root, bw.getDirname())

        if isGstatic:
            from gui.download import downloadGstaticSound
            try:
                downloadGstaticSound(bw.name, os.path.join(curdir, "pronounce.mp3"))
            except:
                # If gstatic pronunciation file is not found, use TTS.
                self.ttscmd(bw.name, bw.editors['name'].langCode, os.path.join(curdir, "pronounce"))
        else:
            self.ttscmd(bw.name, bw.editors['name'].langCode, os.path.join(curdir, "pronounce"))

        wordhead = repeatMp3(os.path.join(curdir, "pronounce.mp3"), self.setting['repeat'])

        sfxdir = self.setting['sfx']
        assert len(sfxdir['word']) != 0, print("Choose at least one sfx accompanying with a word")
        wordheader = os.path.join(curdir, "wordheader.mp3")
        catMp3(os.path.join(self.finalDir, "word-sfx.mp3"), wordhead, wordheader)

        inputs = "%s " % wordheader
        for cont in self.catSequence[bw.name]:
            try:
                cont = cont['def'] + ".mp3"
                inputs += "%s %s " % (os.path.join(self.finalDir, "definition-sfx.mp3"), cont)
            except KeyError:
                cont = cont['ex'] + ".mp3"
                inputs += "%s %s " % (os.path.join(self.finalDir, "example-sfx.mp3"), cont)
        catMp3(inputs, "", os.path.join(self.root, bw.getDirname() + ".mp3"))

    def ttsBundleWidget(self, bw):
        curdir = os.path.join(self.root, bw.getDirname())
        assert os.path.exists(curdir)

        dpw, epd = bw.dpw, bw.epd

        self.catSequence[bw.name] = []

        for i in range(0, dpw):
            define = bw.editors['def-%d' % (i+1)].text()
            defCode = bw.editors['def-%d' % (i+1)].langCode
            if define == '': continue

            filename = os.path.join(curdir, "def-%d" % (i+1))
            self.ttscmd(define, defCode, filename)
            self.catSequence[bw.name].append({"def": filename})

            for j in range(0, epd):
                examp = bw.editors['ex-%d-%d' % (i+1, j+1)].text()
                exCode = bw.editors['ex-%d-%d' % (i+1, j+1)].langCode
                if examp == '': continue

                filename = os.path.join(curdir, "ex-%d-%d" % ((i+1), (j+1)))
                self.ttscmd(examp, exCode, filename)
                self.catSequence[bw.name].append({"ex": filename})


    def mergeDirMp3(self):
        print("Merge all mp3 files in %s" % self.root)
        mergeDirMp3(self.root, self.compMp3)

    def createBgmLoop(self):
        print("Create BGM Loop")
        createLoopMp3(self.root, self.setting['loop'], mp3lenSec(self.compMp3), self.bgmMp3)

    def mixWithBgm(self):
        print("Mix BGM and a-capella mp3")
        mixWithBgm(self.bgmMp3, self.compMp3, self.finalMp3)


def mixWithBgm(bgm, acap, output):
    cmd = "sox -m {bgm} {acapella} {output}".format\
            (bgm=bgm, acapella=acap, output=output)
    call(cmd, shell=True)

def previewTts():
    # FIXME: This is temporal.
    # To be modified to allow users to use various TTS service.
    script = "This is the preview of Text-To-Speech."
    if isLin or isWin:
        cmd = 'espeak "%s"' % script
    elif isMac:
        cmd = 'say "%s"' % script
    else:
        print("Only support Windows, Mac and Linux!")
    call(cmd, shell=True)


####################################
# Fixme:
# Use command-line tool as few as possible
# Remove all redundant use of the tools and put them in a single line.
####################################
def resampling(original, fskhz, output):
    cmd = "sox %s -r %d %s" % (original, fskhz, output)
    call(cmd, shell=True)

def convertBps(original, bitkps, output):
    cmd = "sox %s -C %d %s" % (original, bitkps, output)
    call(cmd, shell=True)

def reduceVolume(original, vol, output):
    # 10/21/17
    # Vol is integer over 0 and 100,
    # Because of the lack of the method to play sound louder in QMediaPlayer,
    # We can only adjust audio files by reducing its volume.
    rate = vol / 100
    cmd = 'ffmpeg -loglevel panic -i {original} -filter:a "volume={rate}" {output}'.format(
                original=original, rate=rate, output=output)
    call(cmd, shell=True)


def createLoopMp3(dir, loop, length, output):
    tmpMp3 = os.path.join(dir, "tmp-bgm-to-remove.mp3")
    if isWin:
        cmd = "type "
    else:
        cmd = "cat "
    bgmlen = 0
    done = False
    while not done:
        for loopInfo in loop:
            bgmlen += loopInfo['duration']
            cmd += "%s " % loopInfo['path']
            if bgmlen > length:
                done = True
                break

    cmd += " > %s" % tmpMp3
    print("create loop by: ", cmd)
    if isWin and bgmlen == loopInfo['duration']:
        # If required bgm length is less than a single loop contents,
        # don't use 'type' (on Windows).
        tmpMp3 = loopInfo['path']
    else:
        call(cmd, shell=True)

    cmd = "ffmpeg -loglevel panic -t %d -i %s -acodec copy %s" % (length, tmpMp3, output)
    call(cmd, shell=True)
    # Fixme; Remove this file
    # call("rm %s" % tmpMp3, shell=True)

def mergeDirMp3(root, output):
    if isWin:
        cmd = "type %s\\*.mp3 > %s" % (root, output)
    else:
        cmd = "cat %s/*.mp3 > %s" % (root, output)
    call(cmd, shell=True)

def espeakMp3(script, langCode, output):
    print("Script: %s (%s)" % (script, langCode))

    os.makedirs(os.path.dirname(output), exist_ok=True)
    if isWin:
        cmd = 'espeak -v {lang} -w {out}.wav "{script}"'.format(
            lang=langCode, out=output, script=script)
        call(cmd, shell=True)
        cmd = 'ffmpeg -loglevel panic -i {out}.wav -ac 2 -ar 44100 -ab 64k -f mp3 {out}.mp3'.format(out=output)
        call(cmd, shell=True)
    else:
        cmd = 'espeak -v {lang} "{script}" --stdout | '.format(lang=langCode, script=script) +\
          'ffmpeg -loglevel panic -i - -ac 2 -ar 44100 -ab 64k -f mp3 %s.mp3' % (output)
        call(cmd, shell=True)


def sayMp3(script, langCode, output):
    print("Script: %s (%s)" % (script, langCode))
    os.makedirs(os.path.dirname(output), exist_ok=True)

    langVersion = {'en': 'Alex',
                   'ja': 'Kyoko ',
                   'ko': 'Yuna',
                   'it': 'Alice',
                   'sv': 'Alva',
                   'fr': 'Thomas',
                   'de': 'Anna',
                   'zh-cn': 'Sin-ji',
                   'hi': 'Lekha',
                   'ru': 'Milena',
                   'ar': 'Maged',
                   'th': 'Kanya',
                   'id': 'Damayanti',
                   'he': 'Carmit',
                   'sk': 'Laura',
                   'eo': 'Monica'}

    try:
        lver = '-v ' + langVersion[langCode]
    except (KeyError, requests.ConnectionError):
        lver = ''
        print("Unsupported language detected: %s" % langCode)

    cmd = 'say %s "%s" -o %s.aiff;' \
          'ffmpeg -loglevel panic -i %s.aiff -ac 2 -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
          % (lver, script, output, output, output)
    call(cmd, shell=True)



def repeatMp3(file, repeat):
    output = "{filename}-{repeat}.mp3".format(filename=file.split('.')[0], repeat=repeat)
    if isWin:
        cmd = "type " + "%s " % file * repeat + "> %s" % output
    else:
        cmd = "cat " + "%s " % file * repeat + "> %s" % output
    call(cmd, shell=True)
    return output


# TODO: Merge two methods below into one
def catMp3(file1, file2, output):
    if isWin:
        cmd = "type %s %s > %s" % (file1, file2, output)
    else:
        cmd = "cat %s %s > %s" % (file1, file2, output)
    print(cmd)
    call(cmd, shell=True)

def catListMp3(filelist, output):
    if isWin:
        cmd = "type "
    else:
        cmd = "cat "
    for file in filelist:
        cmd += "%s " % file
    cmd += "> %s" % output
    call(cmd, shell=True)

def getMp3Info(mp3file):
    duration = hhmmss2sec(mp3Duration(mp3file))

    # Fixme: This is temporal. Need Python coding equivalent to what awk does below.
    if isWin:
        res = str(check_output("ffmpeg -i %s 2>&1 | findstr Stream" % mp3file, shell=True).strip(), 'utf-8')
        info = [res.split(" ")[4], res.split(" ")[8]]
    else:
        info = str(check_output("ffmpeg -i %s 2>&1 | awk '/Stream/' | awk '{print $5, $9}'"
                            % mp3file, shell=True).strip(), 'utf-8').split(" ")
    assert len(info) == 2, 'On %s of %s' % (info, mp3file)
    fskhz, bitkbs = info
    return duration, int(fskhz), int(bitkbs)


def hhmmss2sec(hhmmss):
    # Pythonic implementation of hhmmss2secCmd without OS-based commands
    hr, mi, se, ms = hhmmss.replace(".", ":").split(":")
    return int(hr) * 3600 + int(mi) * 60 + int(se)


def hhmmss2secCmd(hhmmss):
    cmd = 'echo "{hhmmss}" | '.format(hhmmss=hhmmss) + \
          'awk -F: \'{ print ($1 * 3600) + ($2 * 60) + $3 }\''

    return float(check_output(cmd, shell=True))

def soxMp3Duration(mp3file):
    cmd = "soxi %s | grep Duration | awk '{ print $3 }' | tr -d ," % mp3file
    return str(check_output(cmd, shell=True).strip(), 'utf-8')


def mp3Duration(mp3file):
    # SOLVED!
    # Fixme: Why ffmpeg show duration too long (maybe twice longer)
    # This is a bug from ffmpeg and they say users can do nothing.
    # So carefully choose alternative tools such as mutagen.
    # This divided-by-two method is less evident.
    # -- PART 2 --
    # Concatenating mp3 files with the simplest command "cat" causes this problem.
    # And it turned out the duration method has nothing to do with this problem.
    # A solution is to count up the duration of the original mp3 at each time using "cat"
    # -- ANSWER --
    # Difference of bitrate caused the bug.
    # Apparently downloaded audio contents like songs, sfx used 64k of bitrate, then after
    # turning down the bitrate of espeak from 192k to 64k, everything works fine.

    if isWin:
        cmd = "ffmpeg -i %s 2>&1 | findstr Duration" % mp3file
        res = str(check_output(cmd, shell=True).strip(), 'utf-8')
        return res.split("Duration: ")[1].split(",")[0]
    else:
        cmd = "ffmpeg -i %s 2>&1 | grep Duration | awk '{ print $2 }' | tr -d ," % mp3file
        return str(check_output(cmd, shell=True).strip(), 'utf-8')

def mp3lenSec(mp3file):
    return hhmmss2sec(mp3Duration(mp3file))
