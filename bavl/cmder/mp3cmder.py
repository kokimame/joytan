import os, re
from subprocess import call, check_output

from bavl.utils import mkdir, isLin, isMac
from gui.utils import getFileNameFromPath

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
        # Fixme: Name 'seq' somothing more obvious and descriptive
        self.seq = {}
        print(self.setting)

    def setupAudio(self):
        mkdir("{root}/FINAL".format(root=self.root))
        fs = self.setting['sampling']
        bps = self.setting['bitrate']

        for i, songDir in enumerate(self.setting['loop']):
            if songDir['sampling'] != fs:
                output = self.finalDir + "/%s-resamp-%d.mp3" % (songDir['filename'].split(".")[0], i+1)
                resampling(songDir['path'], fs, output)
                songDir['path'] = output
                print("%s resampled!" % songDir['filename'])

        sfxGroup = self.setting['sfx']
        for i, sfxDir in enumerate([sfxGroup['word'], sfxGroup['definitions'], sfxGroup['examples']]):
            if sfxDir['sampling'] != fs:
                output = self.finalDir + "/%s-resamp-%d.mp3" % (sfxDir['filename'].split(".")[0], i+1)
                resampling(sfxDir['path'], fs, output)
                sfxDir['path'] = output
                print("%s resampled!" % sfxDir['filename'])

            if sfxDir['bitrate'] != bps:
                output = self.finalDir + "/%s-bps-%d.mp3" % (sfxDir['filename'].split(".")[0], i+1)
                convertBps(sfxDir['path'], bps, output)
                sfxDir['path'] = output
                print("%s bitrate modified!" % sfxDir['filename'])



    def compileBundle(self, name):
        curdir = '{root}/{name}'.format(root=self.root, name=name)
        assert os.path.exists(curdir + '/gstatic.mp3')

        sfxdir = self.setting['sfx']
        wordhead = repeatMp3(curdir +'/gstatic.mp3', self.setting['repeat'])
        assert sfxdir['word'] != None
        wordheader = curdir + '/wordheader.mp3'
        catMp3(sfxdir['word']['path'], wordhead, wordheader)

        inputs = "%s " % wordheader
        for cont in self.seq[name]:
            try:
                cont = cont['def'] + ".mp3"
                inputs += "%s %s " % (sfxdir['definitions']['path'], cont)
            except KeyError:
                cont = cont['ex'] + ".mp3"
                inputs += "%s %s " % (sfxdir['examples']['path'], cont)
        catMp3(inputs, "", "{root}/{name}.mp3".format(root=self.root, name=name))

    def ttsBundle(self, bundle):
        if isLin:
            ttscmd = espeakMp3
        elif isMac:
            ttscmd = sayMp3
        else:
            raise Exception("Windows is not supported!")


        curdir = "{root}/{name}".format(root=self.root, name=bundle.name)
        assert os.path.exists(curdir)

        dpw, epd = self.setting['dpw'], self.setting['epd']
        self.seq[bundle.name] = []
        for i in range(dpw):
            try:
                define = bundle.items[i]['define']
            except IndexError:
                print("Definitions of '%s' found were less than DPW" % bundle.name)
                continue
            if define == '': continue

            filename = "{dir}/{name}-def-{i}".format(dir=curdir, name=bundle.name, i=(i+1))
            ttscmd(define, filename)
            self.seq[bundle.name].append({"def": filename})

            for j in range(epd):
                examp = bundle.items[i]['example']
                if examp == '': continue

                filename = "{dir}/{name}-ex-{i}-{j}".format\
                    (dir=curdir, name=bundle.name, i=(i+1), j=(j+1))
                ttscmd(examp, filename)
                self.seq[bundle.name].append({"ex": filename})


    def mergeDirMp3(self):
        mergeDirMp3(self.root, self.compMp3)

    def createBgmLoop(self):
        createLoopMp3(self.root, self.setting['loop'], mp3lenSec(self.compMp3), self.bgmMp3)


    def mixWithBgm(self):
        cmd = "sox -m %s %s %s" % (self.bgmMp3, self.compMp3, self.finalMp3)
        call(cmd, shell=True)

def resampling(original, fskhz, output):
    cmd = "sox %s -r %d %s" % (original, fskhz, output)
    call(cmd, shell=True)

def convertBps(original, bitkps, output):
    cmd = "sox %s -C %d %s" % (original, bitkps, output)
    call(cmd, shell=True)

def createLoopMp3(dir, loop, length, output):
    tmpMp3 = "{directory}/temp-bgm-removed.mp3".format(directory=dir)
    cmd = "cat "
    bgmlen = 0
    done = False
    while not done:
        for loopDir in loop:
            bgmlen += loopDir['duration']
            cmd += "%s " % loopDir['path']
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
          'ffmpeg -loglevel panic -i - -ar 44100 -ab 64k -f mp3 %s.mp3' % (script, output)
    call(cmd, shell=True)


def sayMp3(script, output):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    cmd = 'say "%s" -o %s.aiff;' \
          'ffmpeg -loglevel panic -i %s.aiff -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
          % (script, output, output, output)
    call(cmd, shell=True)


def repeatMp3(file, repeat):
    output = "{filename}-{repeat}.mp3".format(filename=file.split('.')[0], repeat=repeat)
    cmd  = "cat " + "%s " % file * repeat  + "> %s" % output
    call(cmd, shell=True)
    return output

def catMp3(file1, file2, output):
    cmd = "cat %s %s > %s" % (file1, file2, output)
    print(cmd)
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
    # This is a bung from ffmpeg and they say users can do nothing.
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
