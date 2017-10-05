from bavl.cmder.mp3cmder import (mixWithBgm, mp3Duration, createLoopMp3, hhmmss2secCmd,
                                catMp3)


loop1 = "/home/kokimame/Emotan/Some-song/anthem/anthem-jp.mp3"
loop2 = "/home/kokimame/Emotan/Some-song/anthem/anthem-us.mp3"

finalmp3 = {"filename": "/home/kokimame/Emotan/workspace/usjp-bgm.mp3", "sec": 300}
intermp3 = "/home/kokimame/Emotan/workspace/usjp-inter-bgm.mp3"

loop = [{"filename": loop1, "sec": hhmmss2secCmd(mp3Duration(loop1))},
        {"filename": loop2, "sec": hhmmss2secCmd(mp3Duration(loop2))}]


cmd = "cat "
bgmlen = 0
done = False
while not done:
    for mp3Dir in loop:
        bgmlen += mp3Dir['sec']
        cmd += "%s " % mp3Dir['filename']
        if bgmlen > finalmp3['sec']:
            done = True
            break
cmd += " > %s" % intermp3

import subprocess
subprocess.call(cmd, shell=True)


cmd = "ffmpeg -loglevel panic -t %d -i %s -acodec copy %s" % (finalmp3['sec'], intermp3, finalmp3['filename'])
subprocess.call(cmd, shell=True)