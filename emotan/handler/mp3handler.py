import os
import pydub
from pydub import AudioSegment as Aseg


class Mp3Handler:
    def __init__(self, setting):
        self.setting = setting
        # Setting Text-to-speech
        self.sfxmap = {}
        self.bgmloop = []
        # List of acapella mp3file (no BGM but with SFX) for each entry
        # Every element is a set of (AudioSegment, QLineEdit.text())
        self.acapellas = []
        self.currentTime = 0
        self.lyrics = []
        self.routers = self._get_routers()

    def _get_routers(self):
        """
        Returns a dict of function to force router to generate audio file
        based on given svc_id, options, path, and text.
        These functions are only compatible with offline TTS service such as
        Say on Mac, espeak on Linux.
        """
        from emotan.speaker import router
        routers = {}
        for key in self.setting['ttsmap']:
            routers[key] = lambda path, text, svc_id=self.setting['ttsmap'][key][1],\
                                  options=self.setting['ttsmap'][key][2]: router.force_run(
                                               svc_id=svc_id,
                                               options=options,
                                               path=path,
                                               text=text)

        return routers

    def setup_audio(self):
        # Setup SFX and BGM by organizing them into groups and adjusting volume.
        for key, sfxinfos in self.setting['sfx'].items():
            if len(sfxinfos) == 0:
                continue
            sfxs = []
            for sfxinfo in sfxinfos:
                sfx = Aseg.from_mp3(sfxinfo['path'])
                vol = self.volume(sfx.dBFS, (1 - sfxinfo['volume'] / 100))
                sfxs.append(sfx - vol)
            self.sfxmap[key] = sum(sfxs)

        for bgminfo in self.setting['loop']:
            bgm = Aseg.from_mp3(bgminfo['path'])
            vol = self.volume(bgm.dBFS, (1 - bgminfo['volume'] / 100))
            self.bgmloop.append(bgm - vol)

    def volume(self, dbfs, percent):
        # Takes dbfs (db relative to full scale, 0 as upper bounds) of the mp3file for volume reducing
        # and the percentage of volume to reduce from the dbfs.
        # The percent is defined by sliders on BarPlayer.

        # Experimental minimum dbfs for human to hear,
        # which corresponds to 0% in percentage
        min_dbfs = -40
        if dbfs < min_dbfs:
            return 0
        return int(abs(min_dbfs - dbfs) * percent)


    def onepass(self, ew):
        # TODO: Create Final.mp3 without generating intermediate mp3files
        # Create complete MP3 contents for an Entry
        # including 3 section; 'atop', 'def-x' and 'ex-x-x'
        asegments = []
        curdir = os.path.join(self.setting['dest'], ew.str_index())
        assert os.path.exists(curdir)

        # If it needs to dictate the index of ew
        if self.setting['idx']:
            idx_file = os.path.join(curdir, "%d") + ".mp3"
            index = "%d " % (ew.row + 1)
            self.routers['atop'](path=idx_file, text=index)
            asegments.append((Aseg.from_mp3(idx_file), index))

        # Atop section
        if "atop" in self.sfxmap:
            asegments.append((self.sfxmap['atop'], None))
        atopText = ew.editors['atop'].text()
        toAtop = os.path.join(curdir, "atop") + ".mp3"

        self.routers['atop'](path=toAtop, text=atopText)
        asegments.append((Aseg.from_mp3(toAtop) * self.setting['repeat'], atopText))

        # Def-x and ex-x-x section
        for i in range(1, ew.lv1 + 1):
            lineKey = 'def-%d' % i
            defText = ew.editors[lineKey].text()
            if defText != '':
                if lineKey in self.sfxmap:
                    asegments.append((self.sfxmap[lineKey], None))
                toDef = os.path.join(curdir, lineKey) + ".mp3"
                self.routers['def-%d' % i](path=toDef, text=defText)
                asegments.append((Aseg.from_mp3(toDef), defText))


            for j in range(1, ew.lv2 + 1):
                lineKey = 'ex-%d-%d' % (i, j)
                exText = ew.editors[lineKey].text()
                if exText != '':
                    if lineKey in self.sfxmap:
                        asegments.append((self.sfxmap[lineKey], None))
                    toEx = os.path.join(curdir, lineKey)
                    self.routers['ex-%d-%d' % (i, j)](path=toEx, text=exText)
                    asegments.append((Aseg.from_mp3(toEx), exText))

        acapella = sum(set[0] for set in asegments)
        if self.setting['lrc']:
            self._add_lyrics(asegments)
        acapella.export(curdir + ".mp3")
        self.acapellas.append(acapella)


    def _add_lyrics(self, asegs):
        for set in asegs:
            aseg, text = set
            if text:
                self.lyrics.append((self.currentTime, text))
            else:
                self.lyrics.append((self.currentTime, ''))
            self.currentTime += len(aseg)

    def write_lyrics(self, output):
        # TODO: WARNING!! May cause encoding bug while handling multi-byte characters
        with open(output, 'w', encoding='utf-8') as lrc:
            for set in self.lyrics:
                mmss = msec2hhmmss(set[0], lrc=True)
                lrc.write("[{time}]{line}\n".format(
                    time=mmss, line=set[1]))

    def get_bgmloop(self, msec):
        done = False
        bl = []
        while not done:
            for bgm in self.bgmloop:
                if msec <= 0:
                    done = True
                    break
                msec -= len(bgm)
                bl.append(bgm)
        return sum(bl)


def get_duration(mp3path, format="hhmmss"):
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
