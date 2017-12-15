import os
import shutil

from subprocess import call, check_output

from gui.utils import getFileNameFromPath, isLin, isMac, isWin
from tools.speaker import Speaker

class Mp3Handler:
    # Do NOT use OS dependent commands in this class method.
    # Those methods with the commands needs to be abstracted.
    def __init__(self, setting):
        self.setting = setting
        self.setting['sampling'] = 44100
        self.setting['bitrate'] = 64
        self.finalDir = os.path.join(self.setting['dest'], "FINAL")
        self.bgmMp3 = os.path.join(self.finalDir, "bgm.mp3")
        # A-capella mp3: TTS voice + SFX without BGM
        self.acapMp3 = os.path.join(self.finalDir, "acap.mp3")
        self.finalMp3 = os.path.join(self.finalDir, "FINAL.mp3")
        self.bitkbs = None  # bit rate (Kbit/s)
        self.fskhz = None      # Sampling rate (kHz)
        # Dictionary that maps editor-contents to TTS-generated mp3 file for each EntryWidget
        self.ewFileMap = {}
        self.sfxMap = {}

        # Setting Text-to-speech
        self.tts = Speaker[self.setting['tts']]()

        print("Audio Setting: ", self.setting)

    def setupAudio(self):
        shutil.rmtree(self.finalDir)
        os.mkdir(self.finalDir)
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

            if not len(sfxlist) == 0:
                self.sfxMap[group] = os.path.join(self.finalDir, group + "-sfx.mp3")
                inputs = ''
                for file in sfxlist:
                    inputs += '%s ' % file
                catMp3(inputs, '', self.sfxMap[group])
            else:
                # If no sfx for a group, store empty string, which will be ignored on concat
                self.sfxMap[group] = ''


    def dictateContents(self, ew):
        curdir = os.path.join(self.setting['dest'], ew.getDirname())
        assert os.path.exists(curdir)

        self.ewFileMap[ew.editors['atop']] = {}

        for i in range(0, ew.dpw):
            define = ew.editors['def-%d' % (i+1)].text()
            if define != '':
                # Fixme: Too complex isn't is? Maybe need a class for storing
                # the relation among content type, language code, label for combobox and
                # voice ID.
                defVid = self.setting['langMap']['def-%d' % (i+1)][1]
                filename = os.path.join(curdir, "def-%d" % (i+1))
                self.tts.dictate(define, defVid, output=filename)
                self.ewFileMap[ew.editors['atop']]['def-%d' % (i + 1)] = filename

            for j in range(0, ew.lv2):
                examp = ew.editors['ex-%d-%d' % (i+1, j+1)].text()
                if examp != '':
                    exVid = self.setting['langMap']['ex-%d-%d' % (i+1, j+1)][1]
                    filename = os.path.join(curdir, "ex-%d-%d" % ((i+1), (j+1)))
                    self.tts.dictate(examp, exVid, output=filename)
                    self.ewFileMap[ew.editors['atop']]['ex-%d-%d' % (i + 1, j + 1)] = filename

    def compileEntry(self, ew, isGstatic=True):
        curdir = os.path.join(self.setting['dest'], ew.getDirname())

        atopLang = self.setting['langMap']['atop'][0]
        atopVid = self.setting['langMap']['atop'][1]
        if isGstatic and (atopLang == 'en'):
            from gui.download import downloadGstaticSound
            try:
                downloadGstaticSound(ew.editors['atop'], os.path.join(curdir, "pronounce.mp3"))
            except:
                # If gstatic pronunciation file is not found, use TTS.
                self.tts.dictate(ew.editors['atop'], atopVid, output=os.path.join(curdir, "pronounce"))
        else:
            self.tts.dictate(ew.editors['atop'], atopVid, output=os.path.join(curdir, "pronounce"))

        pronMp3 = repeatMp3(os.path.join(curdir, "pronounce.mp3"), self.setting['repeat'])

        wordMp3 = os.path.join(curdir, "wordheader.mp3")
        if self.sfxMap['word'] != '':
            catMp3(self.sfxMap['word'], pronMp3, wordMp3)
        else:
            os.rename(pronMp3, wordMp3)

        inputs = "%s " % wordMp3
        fileMap = self.ewFileMap[ew.editors['atop']]
        for i in range(0, ew.lv1):
            try:
                file = fileMap['def-%d' % (i + 1)] + ".mp3"
                inputs += "%s %s " % (self.sfxMap['definition'], file)
            except KeyError:
                pass
            for j in range(0, ew.lv2):
                try:
                    file = fileMap['ex-%d-%d' % (i + 1, j + 1)] + ".mp3"
                    inputs += "%s %s " % (self.sfxMap['example'], file)
                except KeyError:
                    pass

        catMp3(inputs, "", os.path.join(self.setting['dest'], ew.getDirname() + ".mp3"))

    def mergeMp3s(self):
        print("Merge all mp3 files in %s" % self.setting['dest'])
        mergeDirMp3(self.setting['dest'], self.acapMp3)

    def createBgmLoop(self):
        if len(self.setting['loop']) != 0:
            print("Create BGM Loop")
            createLoopMp3(self.setting['dest'], self.setting['loop'], mp3lenSec(self.acapMp3), self.bgmMp3)

    def mixWithBgm(self):
        if len(self.setting['loop']) != 0:
            print("Mix BGM and a-capella mp3")
            mixWithBgm(self.bgmMp3, self.acapMp3, self.finalMp3)
        else:
            # If there is no song for BGM
            os.rename(self.acapMp3, self.finalMp3)


####################################
# FIXME:
# The handler doesn't support filename with whitespaces
# Reading these files stops the app, so
# first implement a way to raise warning message
# if the files are selected and ignore them.
# Then we should have more abstract mp3 handling method in general.
# Using command-line depending on OS requires exhaustive full modification for each OS.
# The solution is to use cross-platform module like pydub.
#
# TODO:
# Use command-line tool as few as possible
# Remove all redundant use of the tools and put them in a single line.
####################################

def mixWithBgm(bgm, acap, output):
    cmd = "sox -m {bgm} {acapella} {output}".format\
            (bgm=bgm, acapella=acap, output=output)
    call(cmd, shell=True)

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
    cmd = "ffmpeg -loglevel panic -i '{original}' -filter:a \"volume={rate}\" {output}".\
            format(original=original, rate=rate, output=output)
    call(cmd, shell=True)


def createLoopMp3(dir, loop, length, output):
    tmpMp3 = os.path.join(dir, "temporal-bgm-to-rm.mp3")
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
        # don't use 'type' (on Windows) for this purpose.
        tmpMp3 = loopInfo['path']
    else:
        call(cmd, shell=True)

    cmd = "ffmpeg -loglevel panic -t %d -i %s -acodec copy %s" % (length, tmpMp3, output)
    call(cmd, shell=True)


def mergeDirMp3(root, output):
    if isWin:
        cmd = "type %s\\*.mp3 > %s" % (root, output)
    else:
        cmd = "cat %s/*.mp3 > %s" % (root, output)
    call(cmd, shell=True)


def repeatMp3(file, repeat):
    output = "{filename}-{repeat}.mp3".format(filename=file.split('.')[0], repeat=repeat)
    if isWin:
        cmd = "type " + "%s " % file * repeat + "> %s" % output
    else:
        cmd = "cat " + "%s " % file * repeat + "> %s" % output
    call(cmd, shell=True)
    return output


def catMp3(file1, file2, output):
    if isWin:
        cmd = "type %s %s > %s" % (file1, file2, output)
    else:
        cmd = "cat %s %s > %s" % (file1, file2, output)
    print(cmd)
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
    # (SOLVED! remained here as a note)
    # Fixme: Why ffmpeg show duration too long (maybe twice longer)
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
