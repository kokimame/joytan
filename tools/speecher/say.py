from tools.speecher import *


class Say(BaseSpeecher):
    def dictate(self, script, lang=None, output=None):
        print("Script: %s (%s)" % (script, lang))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, lang=lang, output=output)

    def save(self, script, lang=None, output=None):
        langVersion = {'en': 'Alex',
                       'ja': 'Kyoko ',
                       'ko': 'Yuna',
                       'it': 'Alice',
                       'sv': 'Alva',
                       'fr': 'Thomas',
                       'de': 'Anna',
                       'zh-cn': 'Sin-ji',
                       'hi': 'Lekha',
                       'ru': 'Milena',
                       'ar': 'Maged',
                       'th': 'Kanya',
                       'id': 'Damayanti',
                       'he': 'Carmit',
                       'sk': 'Laura',
                       'eo': 'Monica'}

        try:
            lver = '-v ' + langVersion[lang]
        except (KeyError):
            lver = ''
            print("Unsupported language detected: %s" % lang)

        cmd = 'say %s "%s" -o %s.aiff;' \
              'ffmpeg -loglevel panic -i %s.aiff -ac 2 -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
              % (lver, script, output, output, output)
        call(cmd, shell=True)
