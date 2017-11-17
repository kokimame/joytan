import os
from subprocess import call, check_output

from gui.utils import getFileNameFromPath, mkdir, isLin, isMac, isWin
from tools.speecher import Speechers

class Mp3Cmder:
    # Do NOT use OS dependent commands in this class method.
    # Those methods with the commands needs to be abstracted.
    def __init__(self, root, setting):
        self.setting = setting
        self.setting['sampling'] = 44100
        self.setting['bitrate'] = 64
        self.root = root
        self.finalDir = os.path.join(self.root, "FINAL")
        self.bgmMp3 = os.path.join(self.finalDir, "bgm.mp3")
        # A-capella mp3: TTS voice + SFX without BGM
        self.acapMp3 = os.path.join(self.finalDir, "acap.mp3")
        self.finalMp3 = os.path.join(self.finalDir, "FINAL.mp3")
        self.bitkbs = None  # bit rate (Kbit/s)
        self.fskhz = None      # Sampling rate (kHz)
        # Dictionary that maps editor-contents to TTS-generated mp3 file for each Bundle widget
        self.bwFileMap = {}
        self.sfxMap = {}

        # Setting Text-to-speech
        self.tts = Speechers[self.setting['tts']]()

        print("Audio Setting: ", self.setting)

    def setupAudio(self):
        mkdir(os.path.join(self.root, "FINAL"))
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


    def dictateContents(self, bw):
        curdir = os.path.join(self.root, bw.getDirname())
        assert os.path.exists(curdir)

        self.bwFileMap[bw.name] = {}

        for i in range(0, bw.dpw):
            define = bw.editors['def-%d' % (i+1)].text()
            if define == '':
                continue
            defLang = self.setting['langMap']['def-%d' % (i+1)]
            filename = os.path.join(curdir, "def-%d" % (i+1))
            self.tts.dictate(define, langCode=defLang, output=filename)
            self.bwFileMap[bw.name]['def-%d' % (i + 1)] = filename

            for j in range(0, bw.epd):
                examp = bw.editors['ex-%d-%d' % (i+1, j+1)].text()
                if examp == '':
                    continue
                exLang = self.setting['langMap']['ex-%d-%d' % (i+1, j+1)]
                filename = os.path.join(curdir, "ex-%d-%d" % ((i+1), (j+1)))
                self.tts.dictate(examp, langCode=exLang, output=filename)
                self.bwFileMap[bw.name]['ex-%d-%d' % (i + 1, j + 1)] = filename

    def compileBundle(self, bw, isGstatic=True):
        curdir = os.path.join(self.root, bw.getDirname())

        langCode = self.setting['langMap']['name']
        if isGstatic and (langCode == 'en'):
            from gui.download import downloadGstaticSound
            try:
                downloadGstaticSound(bw.name, os.path.join(curdir, "pronounce.mp3"))
            except:
                # If gstatic pronunciation file is not found, use TTS.
                self.tts.dictate(bw.name, langCode=langCode, output=os.path.join(curdir, "pronounce"))
        else:
            self.tts.dictate(bw.name, langCode=langCode, output=os.path.join(curdir, "pronounce"))

        pronMp3 = repeatMp3(os.path.join(curdir, "pronounce.mp3"), self.setting['repeat'])

        sfxGroup = self.setting['sfx']
        wordMp3 = os.path.join(curdir, "wordheader.mp3")
        if self.sfxMap['word'] != '':
            catMp3(self.sfxMap['word'], pronMp3, wordMp3)
        else:
            os.rename(pronMp3, wordMp3)

        inputs = "%s " % wordMp3
        fileMap = self.bwFileMap[bw.name]
        for i in range(0, bw.dpw):
            try:
                file = fileMap['def-%d' % (i + 1)] + ".mp3"
                inputs += "%s %s " % (self.sfxMap['definition'], file)
            except KeyError:
                pass
            for j in range(0, bw.epd):
                try:
                    file = fileMap['ex-%d-%d' % (i + 1, j + 1)] + ".mp3"
                    inputs += "%s %s " % (self.sfxMap['example'], file)
                except KeyError:
                    pass

        catMp3(inputs, "", os.path.join(self.root, bw.getDirname() + ".mp3"))

    def mergeMp3s(self):
        print("Merge all mp3 files in %s" % self.root)
        mergeDirMp3(self.root, self.acapMp3)

    def createBgmLoop(self):
        if len(self.setting['loop']) != 0:
            print("Create BGM Loop")
            createLoopMp3(self.root, self.setting['loop'], mp3lenSec(self.acapMp3), self.bgmMp3)

    def mixWithBgm(self):
        if len(self.setting['loop']) != 0:
            print("Mix BGM and a-capella mp3")
            mixWithBgm(self.bgmMp3, self.acapMp3, self.finalMp3)
        else:
            # If there is no song for BGM
            os.rename(self.acapMp3, self.finalMp3)



def mixWithBgm(bgm, acap, output):
    cmd = "sox -m {bgm} {acapella} {output}".format\
            (bgm=bgm, acapella=acap, output=output)
    call(cmd, shell=True)

def previewTts(ttsName):
    script = "This is the preview of Text-To-Speech."
    Speechers[ttsName]().dictate(script, langCode='en')


####################################
# Fixme:
# Use command-line tool as few as possible
# Remove all redundant use of the tools and put them in a single line.
####################################
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
    cmd = 'ffmpeg -loglevel panic -i {original} -filter:a "volume={rate}" {output}'.format(
                original=original, rate=rate, output=output)
    call(cmd, shell=True)


def createLoopMp3(dir, loop, length, output):
    tmpMp3 = os.path.join(dir, "tmp-bgm-to-remove.mp3")
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
        # don't use 'type' (on Windows).
        tmpMp3 = loopInfo['path']
    else:
        call(cmd, shell=True)

    cmd = "ffmpeg -loglevel panic -t %d -i %s -acodec copy %s" % (length, tmpMp3, output)
    call(cmd, shell=True)
    # Fixme; Remove this file
    # call("rm %s" % tmpMp3, shell=True)

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
    # SOLVED!
    # Fixme: Why ffmpeg show duration too long (maybe twice longer)
    # This is a bug from ffmpeg and they say users can do nothing.
    # So carefully choose alternative tools such as mutagen.
    # This divided-by-two method is less evident.
    # -- PART 2 --
    # Concatenating mp3 files with the simplest command "cat" causes this problem.
    # And it turned out the duration method has nothing to do with this problem.
    # A solution is to count up the duration of the original mp3 at each time using "cat"
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
