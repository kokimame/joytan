import os, re
import requests
from subprocess import call, check_output
from googletrans import Translator
from gui.utils import getFileNameFromPath, mkdir, isLin, isMac

class Mp3Cmder:
    def __init__(self, root, setting):
        self.setting = setting
        self.setting['sampling'] = 44100
        self.setting['bitrate'] = 64
        self.root = root
        self.finalDir = "{root}/FINAL".format(root=self.root)
        self.bgmMp3 = '{audio}/bgm.mp3'.format(audio=self.finalDir)
        self.compMp3 = '{audio}/comp.mp3'.format(audio=self.finalDir)
        self.finalMp3 = '{audio}/FINAL.mp3'.format(audio=self.finalDir)
        self.bitkbs = None  # bit rate (Kbit/s)
        self.fskhz = None      # Sampling rate (kHz)
        self.setupAudio()
        # Dictionary to store the sequence of concatenating mp3 files for each word.
        self.catSequence = {}

        if isLin:
            self.ttscmd = espeakMp3
        elif isMac:
            self.ttscmd = sayMp3
        else:
            raise Exception("Windows is not supported!")

        print(self.setting)

    def setupAudio(self):
        mkdir("{root}/FINAL".format(root=self.root))
        fs = self.setting['sampling']
        bps = self.setting['bitrate']

        for i, loop in enumerate(self.setting['loop']):
            if loop['sampling'] != fs:
                output = self.finalDir + "/%s-resamp-%d.mp3" % (loop['filename'].split(".")[0], i+1)
                resampling(loop['path'], fs, output)
                loop['path'] = output
                print("%s resampled!" % loop['filename'])
            if loop['volume'] != 100:
                output = self.finalDir + "/%s-revol-%d.mp3" % (loop['filename'].split(".")[0], i+1)
                reduceVolume(loop['path'], loop['volume'], output)
                loop['path'] = output
                print("%s volume reduced!" % loop['filename'])


        sfxGroup = self.setting['sfx']
        """ {
                'word': [{ ... items ... }, {...},
                'definition' : ...
            }
        """
        for group, sfxs in sfxGroup.items():
            sfxlist = []
            for i, sfxInfo in enumerate(sfxs):
                # Unifying sampling rate
                if sfxInfo['sampling'] != fs:
                    output = self.finalDir + "/%s-resamp-%d.mp3" % (sfxInfo['filename'].split(".")[0], i+1)
                    resampling(sfxInfo['path'], fs, output)
                    sfxInfo['path'] = output
                    sfxInfo['filename'] = getFileNameFromPath(output)
                    print("%s resampled!" % sfxInfo['filename'])

                # Adjusting volume by reducing it
                if sfxInfo['volume'] != 100:
                    output = self.finalDir + "/%s-revol-%d.mp3" % (sfxInfo['filename'].split(".")[0], i+1)
                    reduceVolume(sfxInfo['path'], sfxInfo['volume'], output)
                    sfxInfo['path'] = output
                    print("%s volume reduced!" % sfxInfo['filename'])

                # Unifying bitrate. Bitrate modification is the last otherwise causes mp3 duration bug.
                if sfxInfo['bitrate'] != bps:
                    output = self.finalDir + "/%s-bps-%d.mp3" % (sfxInfo['filename'].split(".")[0], i+1)
                    convertBps(sfxInfo['path'], bps, output)
                    sfxInfo['path'] = output
                    sfxInfo['filename'] = getFileNameFromPath(output)
                    print("%s bitrate modified!" % sfxInfo['filename'])
                sfxlist.append(sfxInfo['path'])
            catListMp3(sfxlist, "{finalDir}/{group}-sfx.mp3".format(finalDir=self.finalDir, group=group))



    def compileBundle(self, bw, isGstatic=True):
        curdir = '{root}/{dirname}'.format(root=self.root, dirname=bw.getDirname())

        if isGstatic:
            from gui.download import downloadGstaticSound
            try:
                downloadGstaticSound(bw.name, "{curdir}/pronounce.mp3".format(curdir=curdir))
            except:
                # If gstatic pronunciation file is not found, use TTS.
                self.ttscmd(bw.name, "{curdir}/pronounce".format(curdir=curdir))
        else:
            self.ttscmd(bw.name, "{curdir}/pronounce".format(curdir=curdir))

        wordhead = repeatMp3('{curdir}/pronounce.mp3'.format(curdir=curdir), self.setting['repeat'])

        sfxdir = self.setting['sfx']
        assert len(sfxdir['word']) != 0, print("Choose at least one sfx accompanying with a word")
        wordheader = '{curdir}/wordheader.mp3'.format(curdir=curdir)
        catMp3("{finalDir}/word-sfx.mp3".format(finalDir=self.finalDir), wordhead, wordheader)

        inputs = "%s " % wordheader
        for cont in self.catSequence[bw.name]:
            try:
                cont = cont['def'] + ".mp3"
                inputs += "%s %s " % ("{finalDir}/definition-sfx.mp3".format(finalDir=self.finalDir), cont)
            except KeyError:
                cont = cont['ex'] + ".mp3"
                inputs += "%s %s " % ("{finalDir}/example-sfx.mp3".format(finalDir=self.finalDir), cont)
        catMp3(inputs, "", "{root}/{dirname}.mp3".format(root=self.root, dirname=bw.getDirname()))

    def ttsBundleWidget(self, bw):
        curdir = "{root}/{dirname}".format(root=self.root, dirname=bw.getDirname())
        assert os.path.exists(curdir)

        dpw, epd = bw.dpw, bw.epd

        self.catSequence[bw.name] = []

        for i in range(1, dpw+1):
            define = bw.editors['def-%d' % i].text()
            if define == '': continue

            filename = "{dir}/def-{i}".format(dir=curdir, i=i)
            self.ttscmd(define, filename)
            self.catSequence[bw.name].append({"def": filename})

            for j in range(1, epd+1):
                examp = bw.editors['ex-%d-%d' % (i, j)].text()
                if examp == '': continue

                filename = "{dir}/ex-{i}-{j}".format\
                    (dir=curdir, i=i, j=j)
                self.ttscmd(examp, filename)
                self.catSequence[bw.name].append({"ex": filename})


    def mergeDirMp3(self):
        mergeDirMp3(self.root, self.compMp3)

    def createBgmLoop(self):
        createLoopMp3(self.root, self.setting['loop'], mp3lenSec(self.compMp3), self.bgmMp3)


    def mixWithBgm(self):
        cmd = "sox -m %s %s %s" % (self.bgmMp3, self.compMp3, self.finalMp3)
        call(cmd, shell=True)

def previewTts():
    script = "This is the preview of Text-To-Speech."
    if isLin:
        cmd = 'espeak "%s"' % script
    elif isMac:
        cmd = 'say "%s"' % script
    else:
        print("Only support Linux and Mac for now!")
    call(cmd, shell=True)


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
    tmpMp3 = "{dir}/tmp-bgm-to-remove.mp3".format(dir=dir)
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
    call(cmd, shell=True)

    cmd = "ffmpeg -loglevel panic -t %d -i %s -acodec copy %s" % (length, tmpMp3, output)
    call(cmd, shell=True)
    call("rm %s" % tmpMp3, shell=True)

def mergeDirMp3(root, output):
    cmd = "cat %s/*.mp3 > %s" % (root, output)
    call(cmd, shell=True)

def espeakMp3(script, output):
    call(["rm", "-f", output])
    os.makedirs(os.path.dirname(output), exist_ok=True)
    cmd = 'espeak "%s" --stdout | ' \
          'ffmpeg -loglevel panic -i - -ac 2 -ar 44100 -ab 64k -f mp3 %s.mp3' % (script, output)
    call(cmd, shell=True)


def sayMp3(script, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)

    langVersion = {'ja': 'Kyoko ',
                   'ko': 'Yuna',
                   'it': 'Alice',
                   'sv': 'Alva',
                   'fr': 'Thomas',
                   'de': 'Anna',
                   'zh': 'Sin-ji',
                   'hi': 'Lekha',
                   'ru': 'Milena',
                   'ar': 'Maged',
                   'th': 'Kanya',
                   'id': 'Damayanti',
                   'he': 'Carmit',
                   'sk': 'Laura',}

    lver = ''
    langCode = ''
    try:
        detect = lambda text: Translator().detect(text).lang
        langCode = detect(script)
        lver = '-v ' + langVersion[langCode]
    except (KeyError, requests.ConnectionError):
        print("Unsupported language detected: %s" % langCode)

    cmd = 'say %s "%s" -o %s.aiff;' \
          'ffmpeg -loglevel panic -i %s.aiff -ac 2 -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
          % (lver, script, output, output, output)
    call(cmd, shell=True)



def repeatMp3(file, repeat):
    output = "{filename}-{repeat}.mp3".format(filename=file.split('.')[0], repeat=repeat)
    cmd  = "cat " + "%s " % file * repeat  + "> %s" % output
    call(cmd, shell=True)
    return output


# TODO: Merge two methods below into one
def catMp3(file1, file2, output):
    cmd = "cat %s %s > %s" % (file1, file2, output)
    print(cmd)
    call(cmd, shell=True)

def catListMp3(filelist, output):
    cmd = "cat "
    for file in filelist:
        cmd += "%s " % file
    cmd += "> %s" % output
    call(cmd, shell=True)

def getMp3Info(mp3file):
    duration = hhmmss2secCmd(mp3Duration(mp3file))
    info = str(check_output("ffmpeg -i %s 2>&1 | awk '/Stream/' | awk '{print $5, $9}'"
                            % mp3file, shell=True).strip(), 'utf-8').split(" ")
    assert len(info) == 2, 'On %s of %s' % (info, mp3file)
    fskhz, bitkbs = info
    return duration, int(fskhz), int(bitkbs)


def hhmmss2sec(hhmmss):
    # Pythonic implementation of hhmmss2secCmd without OS-based commands
    pass


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
    cmd = "ffmpeg -i %s 2>&1 | grep Duration | awk '{ print $2 }' | tr -d ," % mp3file
    return str(check_output(cmd, shell=True).strip(), 'utf-8')


def mp3lenSec(mp3file):
    return hhmmss2secCmd(mp3Duration(mp3file))
