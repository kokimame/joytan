# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import os
import pydub
import tinytag
from pydub import AudioSegment as Aseg


class DubbingWorker:
    """
    This class works in the process of making audiobook, providing an interface for pydub
    """
    def __init__(self, setting):
        self.setting = setting
        self.flowlist = []
        # List of acapella mp3file (without BGM but with SFX) for each entry
        # Every element is a set of (AudioSegment, "corresponding lyrics")
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

    def onepass(self, ew):
        """
        In the process, the worker passes through the parts of each audio segment within
        a given EntryWidget only once, immediately creates a chunk of audio segment which
        will be a part of the actual audiobook (without BGM).
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

        # Concatenate all audio-segment and append it to the interim audiobook (acapellas).
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

    def get_bgmloop(self, audiobook_in_msec):
        """
        Generate looped BGM within given millisecond with user-selected songs.
        BGM may contain very long audio files which exceed the duration of
        the audiobook we are making. Loading such file as a whole using pydub
        is not time effective, so in these situation we call ffmpeg command to 
        copy and split the song into the size of what we need.
        """

        done = False
        bgmloop = []
        def remaining():
            return max(audiobook_in_msec - sum([len(aseg) for aseg in bgmloop]), 0)

        while not done:
            # Reading flowitem from audio dialog setting
            for fi in self.setting['loop']:
                if fi['desc'] == "MP3":
                    duration = duration_tag(fi['path'])
                    if duration > remaining():
                        output = os.path.join(self.setting['dest'], 'last_fraction_bgm.mp3')
                        copy_and_split(fi['path'], output, remaining())
                        bgm = Aseg.from_mp3(output)
                        rdbfs = reduce_dbfs(bgm.dBFS, (1 - fi['volume'] / 100))
                        bgmloop.append((bgm - rdbfs))
                        done = True
                    else:
                        bgm = Aseg.from_mp3(fi['path'])
                        rdbfs = reduce_dbfs(bgm.dBFS, (1 - fi['volume'] / 100))
                        # Probably it's save to overlay even if BGM exceeds msec with
                        # the repetition below.
                        for _ in range(fi['repeat']):
                            if not remaining():
                                done = True
                                break
                            bgmloop.append((bgm - rdbfs))
                            if fi['postrest'] > 0:
                                bgmloop.append(Aseg.silent(int(fi['postrest'] * 1000)))
                elif fi['desc'] == "REST" and fi['postrest'] > 0:
                    bgmloop.append(Aseg.silent(int(fi['postrest'] * 1000)))
                if done or not remaining():
                    break

        return sum(bgmloop)

def copy_and_split(mp3path, output, ending):
    """
    :param mp3path: Path to mp3 file to copy and cut
    :param output: Path to output mp3 file
    :param ending: Time to cut(split) input mp3file

    This gets called when the duration of a song at the end exceeds the 
    remaining time we need while making a looped BGM.
    This copies input mp3file and cuts it at given time then save it as 'output'. 
    """
    program = pydub.utils.which("ffmpeg")
    command = [program,
               '-y',  # Say yes to override confirmation
               '-i', mp3path,
               '-acodec', 'copy',
               '-loglevel', 'panic',
               '-ss', '0',
               '-to', str(ending / 1000),
               output]

    import subprocess
    subprocess.call(command)

def duration_tag(mp3path):
    """
    Returns the duration of given mp3 file in millisecond
    """
    Tag = tinytag.TinyTag.get(mp3path)
    return Tag.duration * 1000

def reduce_dbfs(dbfs, percent):
    """
    :param dbfs: decibel relative to full scale, 0 as upper bounds
    :param percent: The percentage of volume to reduce from the dbfs
    :return: Integer of dbfs to reduce
    
    Calculate dbfs to reduce by given percentage.
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
