import os
import pydub
from pydub import AudioSegment as Aseg


class Mp3Handler:
    def __init__(self, setting):
        self.setting = setting
        self.flowlist = []
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
        from joytan.speaker import router
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
        # Setup SFX and BGM by converting them in AudioSegement and adjusting volume.
        for fi in self.setting['flow']:
            if fi['desc'] == "MP3":
                sfx = Aseg.from_mp3(fi['path'])
                volume = self._volume(sfx.dBFS, (1 - fi['volume']/100))
                self.flowlist.append(sfx - volume)
            elif fi['desc'] == "REST":
                silence = Aseg.silent(int(fi['duration'] * 1000))
                self.flowlist.append(silence)
            else:
                # Write a signal of ewkey object to be dictated on onepass process
                self.flowlist.append(fi['desc'])

        for fi in self.setting['loop']:
            if fi['desc'] == "MP3":
                bgm = Aseg.from_mp3(fi['path'])
                volume = self._volume(bgm.dBFS, (1 - fi['volume']/100))
                self.bgmloop.append(bgm - volume)
            elif fi['desc'] == "REST":
                silence = Aseg.silent(int(fi['duration'] * 1000))
                self.bgmloop.append(silence)

    def _volume(self, dbfs, percent):
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
        # Create an entire MP3 material for an Entry
        asegments = []
        curdir = os.path.join(self.setting['dest'], ew.str_index())
        assert os.path.exists(curdir)

        for fi in self.flowlist:
            if isinstance(fi, Aseg):
                asegments.append((fi, ''))
                continue

            assert isinstance(fi, str)
            if fi == 'INDEX':
                index = "%d " % (ew.row + 1)
                idx_file = os.path.join(curdir, "index") + ".mp3"
                self.routers['atop'](path=idx_file, text=index)
                asegments.append((Aseg.from_mp3(idx_file), index))
            else:
                ewkey = fi
                path = os.path.join(curdir, ewkey) + ".mp3"
                text = ew.editors[ewkey].text()
                if text != '':
                    self.routers[ewkey](path=path, text=text)
                    asegments.append((Aseg.from_mp3(path), text))

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
