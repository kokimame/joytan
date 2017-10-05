from bavl.cmder.mp3cmder import *


def espeakMp3(script, output):
    call(["rm", "-f", output])
    os.makedirs(os.path.dirname(output), exist_ok=True)
    cmd = 'espeak "%s" --stdout | ' \
          'ffmpeg -loglevel panic -i - -ar 44100 -ab 64k -ac 2 -f mp3 %s.mp3' % (script, output)
    call(cmd, shell=True)


espeakMp3("Hello, I'm espeak, born in open-source, and totally free!", "./mp3samples/hello-espeak")

amp3 = "./mp3samples/misc/hello-espeak.mp3"
bmp3 = "./mp3samples/sfx/basic/SPRING_B.mp3"
cmp3 = "./mp3samples/misc/catSfx2.mp3"

from subprocess import check_output, call

# call("ffmpeg -i %s 2>&1 | awk '/Duration/,/Stream/'" % bmp3, shell=True)
call("ffmpeg -i %s 2>&1 | awk '/Duration/,/Stream/'" % amp3, shell=True)
# call("ffmpeg -i %s 2>&1 | awk '/Duration/,/Stream/'" % cmp3, shell=True)
call("ffmpeg -i %s 2>&1 | awk '/Duration/' | awk '{print $2}' | tr -d ," % amp3, shell=True)
info = str(check_output("ffmpeg -i %s 2>&1 | awk '/Stream/' | awk '{print $5, $9}'"
                        % amp3, shell=True).strip(), "utf-8")
print(info.split(" "))
