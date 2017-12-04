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

    def setupAudio(self):
        sfxMap = self.setting['sfx']
        #
        #
        # TODO: Ajusting volume, combining into one SFX for each lineKey
        #
        #
        for key, sfxInfos in sfxMap.items():
            if len(sfxInfos) == 0:
                continue
            self.sfxMap[key] = sum([Aseg.from_mp3(info['path']) for info in sfxInfos])


    def runSpeaker(self, ew):
        print(self.sfxMap)
        curdir = os.path.join(self.setting['dest'], ew.getDirname())
        assert os.path.exists(curdir)
        asegList = []

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

        print(asegList)
        sum(asegList).export(curdir + ".mp3", format="mp3")

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
