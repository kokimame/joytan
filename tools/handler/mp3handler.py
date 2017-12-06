import os
import pydub
from pydub import AudioSegment as Aseg

from tools.speaker import Speaker

class Mp3Handler:
    def __init__(self, setting):
        self.setting = setting
        # Setting Text-to-speech
        self.tts = Speaker[self.setting['tts']]()
        self.sfxMap = {}
        self.bgmLoop = []
        # List of acapella mp3file (no BGM but with SFX) for each entry
        # Every element is a set of (AudioSegment, QLineEdit.text())
        self.acapList = []
        self.currentTime = 0
        self.needsLrc = self.setting['lrc']
        self.lrcFormat = []

    def setupAudio(self):
        # Setup SFX and BGM by organizing them into groups and adjusting volume.
        for key, sfxInfos in self.setting['sfx'].items():
            if len(sfxInfos) == 0:
                continue
            sfxs = []
            for sfxInfo in sfxInfos:
                sfx = Aseg.from_mp3(sfxInfo['path'])
                vtr = self.volToReduce(sfx.dBFS, (1 - sfxInfo['volume']/100))
                sfxs.append(sfx - vtr)
            self.sfxMap[key] = sum(sfxs)

        for bgmInfo in self.setting['loop']:
            bgm = Aseg.from_mp3(bgmInfo['path'])
            vtr = self.volToReduce(bgm.dBFS,(1 - bgmInfo['volume']/100))
            self.bgmLoop.append(bgm - vtr)

    def volToReduce(self, dBFS, percent):
        # Takes dBFS (db relative to full scale, 0 as upper bounds) of the mp3file for volume reducing
        # and the percentage of volume to reduce from the dBFS.
        # The percent is defined by sliders on Mp3Widget.

        # Experimental minimum dBFS for human to hear,
        # which corresponds to 0% in percentage
        minDbfs = -40
        if dBFS < minDbfs:
            return 0
        return int(abs(minDbfs - dBFS) * percent)


    def runSpeaker(self, ew):
        # TODO: Create Final.mp3 without generating intermediate mp3files
        # Create complete MP3 contents for an Entry
        # including 3 section; 'atop', 'def-x' and 'ex-x-x'
        curdir = os.path.join(self.setting['dest'], ew.getDirname())
        assert os.path.exists(curdir)
        asegList = []

        # Atop section
        if "atop" in self.sfxMap:
            asegList.append((self.sfxMap['atop'], None))
        atopLang, atopVid = self.setting['langMap']['atop']
        atopText = ew.editors['atop'].text()
        toAtop = os.path.join(curdir, "atop")

        if self.setting['gstatic'] and (atopLang == 'en'):
            from gui.download import downloadGstaticSound
            try:
                downloadGstaticSound(atopText, toAtop + ".mp3")
            except:
                # If gstatic pronunciation file is not found, use TTS.
                self.tts.dictate(atopText, atopVid, output=toAtop)
        else:
            self.tts.dictate(atopText, atopVid, output=toAtop)

        asegList.append((Aseg.from_mp3(toAtop + ".mp3") * self.setting['repeat'], atopText))

        # Def-x and ex-x-x section
        for i in range(0, ew.dpw):
            lineKey = 'def-%d' % (i+1)
            defText = ew.editors[lineKey].text()
            if defText != '':
                if lineKey in self.sfxMap:
                    asegList.append((self.sfxMap[lineKey], None))
                defVid = self.setting['langMap'][lineKey][1]
                toDef = os.path.join(curdir, lineKey)
                # TODO: Rename 'dictate' to 'speak' or 'run'
                self.tts.dictate(defText, defVid, output=toDef)
                asegList.append((Aseg.from_mp3(toDef + ".mp3"), defText))

            for j in range(0, ew.epd):
                lineKey = 'ex-%d-%d' % (i + 1, j + 1)
                exText = ew.editors[lineKey].text()
                if exText != '':
                    if lineKey in self.sfxMap:
                        asegList.append((self.sfxMap[lineKey], None))
                    exVid = self.setting['langMap'][lineKey][1]
                    toEx = os.path.join(curdir, lineKey)
                    self.tts.dictate(exText, exVid, output=toEx)
                    asegList.append((Aseg.from_mp3(toEx + ".mp3"), exText))

        acapella = sum(set[0] for set in asegList)
        if self.needsLrc:
            self.addLyrics(asegList)
        acapella.export(curdir + ".mp3")
        self.acapList.append(acapella)


    def addLyrics(self, asegs):
        for set in asegs:
            aseg, text = set
            if text:
                self.lrcFormat.append((self.currentTime, text))
            else:
                self.lrcFormat.append((self.currentTime, ''))
            self.currentTime += len(aseg)

    def writeLyrics(self, output):
        with open(output, 'w') as lrc:
            for set in self.lrcFormat:
                mmss = msec2hhmmss(set[0], lrc=True)
                lrc.write("[{time}]{line}\n".format(
                    time=mmss, line=set[1]))



    def getBgmLoop(self, msec):
        done = False
        bl = []
        while not done:
            for bgm in self.bgmLoop:
                if msec <= 0:
                    done = True
                    break
                msec -= len(bgm)
                bl.append(bgm)
        return sum(bl)


def getMp3Duration(mp3path, format="hhmmss"):
    if format == "msec":
        return len(Aseg.from_mp3(mp3path))
    elif format == "hhmmss":
        return msec2hhmmss(len(Aseg.from_mp3(mp3path)))
    else:
        raise Exception("Error: Wrong Duration format selected")

def msec2hhmmss(msec, lrc=False):
    sec = msec / 1000
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    mmss = "%02d:%02d" % (m, s)
    if lrc:
        mmss += ".%02d" % (msec % 100)
        return mmss
    hhmmss = "%02d:%02d:%02d" % (h, m, s)
    return hhmmss
