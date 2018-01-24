# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import os
import pydub
from pydub import AudioSegment as Aseg


class DubbingWorker:
    """
    This class works in the process of making audiobook, providing an interface for pydub
    """
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
        Returns a dict of function to force router of AwesomeTTS to generate audio clips
        based on given svc_id, options, path, and text.
        These functions are only compatible with offline TTS service such as
        Say on Mac, espeak on Linux.
        """
        from joytan.speaker import router

        def force_run(svc_id, options, path, text):
            try:
                router.force_run(svc_id, options, path, text)
            except:
                #Any exception is thrown to the screen as a critical message,
                #then the dubbing thread will immediately be killed.
                raise

        routers = {}
        for key in self.setting['ttsmap']:
            routers[key] = lambda path, text, svc_id=self.setting['ttsmap'][key][1],\
                                  options=self.setting['ttsmap'][key][2]: force_run(
                                               svc_id=svc_id,
                                               options=options,
                                               path=path,
                                               text=text)

        return routers

    def setup_audio(self):
        """
        Setup SFX and BGM by converting them in AudioSegment and adjusting volume.
        """
        for fi in self.setting['flow']:
            if fi['desc'] == "MP3":
                sfx = Aseg.from_mp3(fi['path'])
                rdbfs = reduce_dbfs(sfx.dBFS, (1 - fi['volume'] / 100))
                for _ in range(fi['repeat']):
                    self.flowlist.append((sfx - rdbfs))
                    if fi['postrest'] > 0:
                        self.flowlist.append(Aseg.silent(int(fi['postrest'] * 1000)))

            elif fi['desc'] == "REST" and fi['postrest'] > 0:
                self.flowlist.append(Aseg.silent(int(fi['postrest'] * 1000)))
            else:
                # Audio segments for index and ewkeys are generated dynamically on onepass
                self.flowlist.append(fi)

        # FIXME: Creating BGM loop should be done after finding the acapella audio duration
        for fi in self.setting['loop']:
            if fi['desc'] == "MP3":
                bgm = Aseg.from_mp3(fi['path'])
                rdbfs = reduce_dbfs(bgm.dBFS, (1 - fi['volume'] / 100))
                for _ in range(fi['repeat']):
                    self.bgmloop.append((bgm - rdbfs))
                    if fi['postrest'] > 0:
                        self.bgmloop.append(Aseg.silent(int(fi['postrest'] * 1000)))
            elif fi['desc'] == "REST" and fi['postrest'] > 0:
                self.bgmloop.append(Aseg.silent(int(fi['postrest'] * 1000)))

    def onepass(self, ew):
        """
        In the process, the worker passes through the parts of each audio segment within
        a given EntryWidget only once, immediately creates bigger chunk of audio segment and
        appends it to the interim audiobook, acapella.
        """
        # This contains a list of set(audio object from pydub, corresponding string text)
        asegments = []
        curdir = os.path.join(self.setting['dest'], ew.str_index())
        assert os.path.exists(curdir)

        for fi in self.flowlist:
            if isinstance(fi, Aseg):
                asegments.append((fi, ''))
                continue

            if fi['desc'] == 'INDEX':
                index = "%d " % (ew.row + 1)
                idx_file = os.path.join(curdir, "index") + ".mp3"
                self.routers['atop'](path=idx_file, text=index)
                for _ in range(fi['repeat']):
                    aseg = Aseg.from_mp3(idx_file)
                    rdbfs = reduce_dbfs(aseg.dBFS, (1 - fi['volume'] / 100))
                    asegments.append((aseg - rdbfs, index))
                    if fi['postrest'] > 0:
                        asegments.append((Aseg.silent(int(fi['postrest'] * 1000)), ''))

            else:
                ewkey = fi['desc']
                path = os.path.join(curdir, ewkey) + ".mp3"
                if ew[ewkey] != '':
                    self.routers[ewkey](path=path, text=ew[ewkey])
                    for _ in range(fi['repeat']):
                        aseg = Aseg.from_mp3(path)
                        rdbfs = reduce_dbfs(aseg.dBFS, (1 - fi['volume'] / 100))
                        asegments.append((aseg - rdbfs, ew[ewkey]))
                        if fi['postrest'] > 0:
                            asegments.append((Aseg.silent(int(fi['postrest'] * 1000)), ''))

        # '>><<' represents the end of one EntryWidget.
        # This lets you know the timing to switch images on video-making
        asegments.append((Aseg.silent(0), '>><<'))

        # Concatenate all audio-segment to make audiobook without BGM
        acapella = sum(item[0] for item in asegments)
        if self.setting['lrc']:
            self._add_lyrics(asegments)
        acapella.export(curdir + ".mp3")
        self.acapellas.append(acapella)

    def _add_lyrics(self, asegs):
        """
        Updates lyrics text and lyrics timer for given Entry's audio-segments
        """
        for item in asegs:
            aseg, text = item
            if text:
                self.lyrics.append((self.currentTime, text))
            else:
                self.lyrics.append((self.currentTime, ''))
            self.currentTime += len(aseg)

    def make_lyrics(self, output):
        """
        Audio dialog calls this method to complete and output LRC file 
        """
        with open(output, 'w', encoding='utf-8') as lrc:
            for item in self.lyrics:
                mmss = msec2hhmmss(item[0], lrc=True)
                lrc.write("[{time}]{line}\n".format(
                    time=mmss, line=item[1]))

    def get_bgmloop(self, msec):
        """
        Generate looped BGM within given millisecond with user-selected songs
        """
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


def reduce_dbfs(dbfs, percent):
    """
    :param dbfs: decibel relative to full scale, 0 as upper bounds
    :param percent: The percentage of volume to reduce from the dbfs
    :return: Integer of dbfs after reducing volume by the percentage
    
    Reduce dbFS by given percentage amount.
    """
    # Experimental least dbfs of sounds which human can hear.
    # This is intended to correspond to the 'volume 0% (mute)'.
    # However, it turns out -40 is wrong to achieve this goal;
    # even if volume slider is set to 0, you can slightly hear sounds.
    # But coming to think of the fact if you want to mute an audio just
    # delete it, and lacking the info of how to mute by reducing dbfs,
    # min_dbfs is set to -40 for time being.
    min_dbfs = -40
    if dbfs < min_dbfs:
        return 0
    return int(abs(min_dbfs - dbfs) * percent)


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
