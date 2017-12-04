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

    def setupAudio(self):
        pass

    def runSpeaker(self, ew):
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

        asegList.append(Aseg.from_mp3(toAtop + ".mp3") * self.setting['repeat'])

        for i in range(0, ew.dpw):
            defText = ew.editors['def-%d' % (i+1)].text()
            if defText != '':
                defVid = self.setting['langMap']['def-%d' % (i+1)][1]
                toDef = os.path.join(curdir, "def-%d" % (i+1))
                # TODO: Rename 'dictate' to 'speak' or 'run'
                self.tts.dictate(defText, defVid, output=toDef)
                asegList.append(Aseg.from_mp3(toDef + ".mp3"))

            for j in range(0, ew.epd):
                exText = ew.editors['ex-%d-%d' % (i+1, j+1)].text()
                if exText != '':
                    exVid = self.setting['langMap']['ex-%d-%d' % (i+1, j+1)][1]
                    toEx = os.path.join(curdir, "ex-%d-%d" % ((i+1), (j+1)))
                    self.tts.dictate(exText, exVid, output=toEx)
                    asegList.append(Aseg.from_mp3(toEx + ".mp3"))

        sum(asegList).export(curdir + ".mp3", format="mp3")
