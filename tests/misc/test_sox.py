
amp3 = "./mp3samples/hello-espeak.mp3"
bmp3 = "./mp3samples/song/touch.mp3"
cmp3 = "./mp3samples/soxTest.mp3"

cmd = "sox -m %s %s %s" % (amp3, bmp3, cmp3)

from subprocess import call
call(cmd, shell=True)