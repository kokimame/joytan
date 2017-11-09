from tools.speecher import *


class Say(BaseSpeecher):
    langPpl = {'en': 'Alex',
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


    def dictate(self, script, lang=None, output=None):
        print("Script: %s (%s)" % (script, lang))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, lang=lang, output=output)

        else:
            ppl = self.code2ppl(lang)
            call('say %s "%s"' % (ppl, script), shell=True)

    def save(self, script, lang=None, output=None):
        ppl = self.code2ppl(lang)
        cmd = 'say %s "%s" -o %s.aiff;' \
              'ffmpeg -loglevel panic -i %s.aiff -ac 2 -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
              % (ppl, script, output, output, output)
        call(cmd, shell=True)

    def code2ppl(self, lang):
        try:
            ppl = '-v ' + self.langPpl[lang]
        except (KeyError):
            ppl = ''
            print("Unsupported language detected: %s" % lang)
        return ppl