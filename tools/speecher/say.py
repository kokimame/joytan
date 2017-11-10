from tools.speecher import *


def getVoiceInfo():
    info = str(check_output("say -v ?", shell=True), 'utf-8').strip().split('\n')
    info = [' '.join(row.split()) for row in info]
    vd = {}
    for line in info:
        combo, example = line.split(' # ')
        vd[combo] = example
    return vd


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

    # We want to call 'say -v ?' only once at runtime.
    # Don't call the command every time voice type changed.
    from gui.utils import isMac
    if isMac:
        # voiceCombo has voice names shown in a combobox on Preferences
        voiceInfo = getVoiceInfo()
        voiceCombo = voiceInfo.keys()

    def dictate(self, script, lang=None, output=None):
        print("Script: %s (%s)" % (script, lang))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, output, lang=lang)

        else:
            ppl = self.code2ppl(lang)
            call('say %s "%s"' % (ppl, script), shell=True)

    def save(self, script, output, lang=None):
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

    # Actually pre'listen' though.
    def preview(self, combo):
        script = self.voiceInfo[combo]
        combo = combo.split(' ')
        name = ' '.join(combo[0: len(combo) - 1])
        lang = combo[-1].split('_')
        call('say -v {name} "{script}"'.format(name=name, script=script), shell=True)
