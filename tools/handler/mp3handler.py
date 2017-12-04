import os
import pydub
from gui.utils import mkdir
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
        self.acapList = []

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
        # The percent is defined by sliderson Mp3Widget.

        # Experimental minimum dBFS for human to hear,
        # which corresponds to 0 in percentage
        minDbfs = -50
        if dBFS < minDbfs:
            return 0
        return int(abs(minDbfs - dBFS) * percent)


    def runSpeaker(self, ew):
        # TODO: Create Final.mp3 without generating intermediate mp3files
        # Create complete audio contents in MP3 of an Entry
        # including 3 section; 'atop', 'def-x' and 'ex-x-x'
        curdir = os.path.join(self.setting['dest'], ew.getDirname())
        assert os.path.exists(curdir)
        asegList = []

        # Atop section
        atopLang, atopVid = self.setting['langMap']['atop']
        toAtop = os.path.join(curdir, "atop")

        if self.setting['gstatic'] and (atopLang == 'en'):
            from gui.download import downloadGstaticSound
            try:
                downloadGstaticSound(ew.atop, toAtop + ".mp3")
            except:
                # If gstatic pronunciation file is not found, use TTS.
                self.tts.dictate(ew.atop, atopVid, output=toAtop)
        else:
            self.tts.dictate(ew.atop, atopVid, output=toAtop)

        if "atop" in self.sfxMap:
            asegList.append(self.sfxMap['atop'])
        asegList.append(Aseg.from_mp3(toAtop + ".mp3") * self.setting['repeat'])

        # Def-x and ex-x-x section
        for i in range(0, ew.dpw):
            lineKey = 'def-%d' % (i+1)
            defText = ew.editors[lineKey].text()
            if defText != '':
                defVid = self.setting['langMap'][lineKey][1]
                toDef = os.path.join(curdir, lineKey)
                # TODO: Rename 'dictate' to 'speak' or 'run'
                self.tts.dictate(defText, defVid, output=toDef)
                if lineKey in self.sfxMap:
                    asegList.append(self.sfxMap[lineKey])
                asegList.append(Aseg.from_mp3(toDef + ".mp3"))

            for j in range(0, ew.epd):
                lineKey = 'ex-%d-%d' % (i + 1, j + 1)
                exText = ew.editors[lineKey].text()
                if exText != '':
                    exVid = self.setting['langMap'][lineKey][1]
                    toEx = os.path.join(curdir, lineKey)
                    self.tts.dictate(exText, exVid, output=toEx)
                    if lineKey in self.sfxMap:
                        asegList.append(self.sfxMap[lineKey])
                    asegList.append(Aseg.from_mp3(toEx + ".mp3"))

        acapella = sum(asegList)
        acapella.export(curdir + ".mp3")
        self.acapList.append(acapella)

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

def msec2hhmmss(msec):
    sec = msec / 1000
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)
