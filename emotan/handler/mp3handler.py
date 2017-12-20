import os
import pydub
from pydub import AudioSegment as Aseg


class Mp3Handler:
    def __init__(self, setting):
        self.setting = setting
        # Setting Text-to-speech
        self.sfxMap = {}
        self.bgmLoop = []
        # List of acapella mp3file (no BGM but with SFX) for each entry
        # Every element is a set of (AudioSegment, QLineEdit.text())
        self.acapList = []
        self.currentTime = 0
        self.lrcFormat = []
        self.routers = self.getRouters()

    def getRouters(self):
        """
        Returns a dict of function to force router to generate audio file
        based on given svc_id, options, path, and text.
        These functions are only compatible with offline TTS service such as
        Say on Mac, espeak on Linux.
        """
        from emotan.speaker import router
        routers = {}
        for key in self.setting['ttsMap']:
            routers[key] = lambda path, text, svc_id=self.setting['ttsMap'][key][1],\
                                  options=self.setting['ttsMap'][key][2]: router.force_run(
                                               svc_id=svc_id,
                                               options=options,
                                               path=path,
                                               text=text)
            print(self.setting['ttsMap'][key][2])
            print(key)
        print(routers)

        return routers



    def setupAudio(self):
        # Setup SFX and BGM by organizing them into groups and adjusting volume.
        for key, sfxInfos in self.setting['sfx'].items():
            if len(sfxInfos) == 0:
                continue
            sfxs = []
            for sfxInfo in sfxInfos:
                sfx = Aseg.from_mp3(sfxInfo['path'])
                vol = self.volume(sfx.dBFS, (1 - sfxInfo['volume'] / 100))
                sfxs.append(sfx - vol)
            self.sfxMap[key] = sum(sfxs)

        for bgmInfo in self.setting['loop']:
            bgm = Aseg.from_mp3(bgmInfo['path'])
            vol = self.volume(bgm.dBFS, (1 - bgmInfo['volume'] / 100))
            self.bgmLoop.append(bgm - vol)

    def volume(self, dBFS, percent):
        # Takes dBFS (db relative to full scale, 0 as upper bounds) of the mp3file for volume reducing
        # and the percentage of volume to reduce from the dBFS.
        # The percent is defined by sliders on Mp3Widget.

        # Experimental minimum dBFS for human to hear,
        # which corresponds to 0% in percentage
        minDbfs = -40
        if dBFS < minDbfs:
            return 0
        return int(abs(minDbfs - dBFS) * percent)


    def onepass(self, ew):
        # TODO: Create Final.mp3 without generating intermediate mp3files
        # Create complete MP3 contents for an Entry
        # including 3 section; 'atop', 'def-x' and 'ex-x-x'
        asegList = []
        curdir = os.path.join(self.setting['dest'], ew.stringIndex())
        assert os.path.exists(curdir)

        # If it needs to dictate the index of ew
        if self.setting['idx']:
            idx_file = os.path.join(curdir, "%d") + ".mp3"
            index = "%d " % (ew.row + 1)
            self.routers['atop'](path=idx_file, text=index)
            asegList.append((Aseg.from_mp3(idx_file), index))

        # Atop section
        if "atop" in self.sfxMap:
            asegList.append((self.sfxMap['atop'], None))
        atopText = ew.editors['atop'].text()
        toAtop = os.path.join(curdir, "atop") + ".mp3"

        self.routers['atop'](path=toAtop, text=atopText)
        asegList.append((Aseg.from_mp3(toAtop) * self.setting['repeat'], atopText))

        # Def-x and ex-x-x section
        for i in range(1, ew.lv1 + 1):
            lineKey = 'def-%d' % i
            defText = ew.editors[lineKey].text()
            if defText != '':
                if lineKey in self.sfxMap:
                    asegList.append((self.sfxMap[lineKey], None))
                toDef = os.path.join(curdir, lineKey) + ".mp3"
                self.routers['def-%d' % i](path=toDef, text=defText)
                asegList.append((Aseg.from_mp3(toDef), defText))


            for j in range(1, ew.lv2 + 1):
                lineKey = 'ex-%d-%d' % (i, j)
                exText = ew.editors[lineKey].text()
                if exText != '':
                    if lineKey in self.sfxMap:
                        asegList.append((self.sfxMap[lineKey], None))
                    toEx = os.path.join(curdir, lineKey)
                    self.routers['ex-%d-%d' % (i, j)](path=toEx, text=exText)
                    asegList.append((Aseg.from_mp3(toEx), exText))

        acapella = sum(set[0] for set in asegList)
        if self.setting['lrc']:
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
        # TODO: WARNING!! May cause encoding bug while handling multi-byte characters
        with open(output, 'w', encoding='utf-8') as lrc:
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
