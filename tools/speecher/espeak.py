
from tools.speecher import *

class Espeak(BaseSpeecher):
    def __init__(self):
        pass

    def dictate(self, script, lang=None, output=None):
        print("Script: %s (%s)" % (script, lang))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, lang=lang, output=output)
            return

        else:
            cmd = 'espeak -v {lang} "{script}"'.format(lang=lang, script=script)
            call(cmd, shell=True)


    def save(self, script, lang=None, output=None):
        if isWin:
            cmd = 'espeak -v {lang} -w {out}.wav "{script}"'.format(lang=lang, out=output, script=script)
            call(cmd, shell=True)
            cmd = 'ffmpeg -loglevel panic -i {out}.wav -ac 2 -ar 44100 -ab 64k -f mp3 {out}.mp3'.format(out=output)
            call(cmd, shell=True)
        else:
            cmd = 'espeak -v {lang} "{script}" --stdout | '.format(lang=lang, script=script) + \
                  'ffmpeg -loglevel panic -i - -ac 2 -ar 44100 -ab 64k -f mp3 %s.mp3' % (output)
            call(cmd, shell=True)


    def isSupported(self):
        raise NotImplementedError