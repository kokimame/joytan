from tools.speecher import *
from gui.utils import LANGUAGES

def getTtsHelp():
    # Returns ['langCode', 'Voice name', 'Voice name + detail langCode (Shown in Combobox)', 'example']
    i1 = str(check_output("say -v ?", shell=True), 'utf-8').strip().split('\n')
    i2 = [' '.join(row.split()) for row in i1]
    i3 = []
    for i in i2:
        combo, examp = i.split(' # ')
        i4 = combo.split(' ')
        if len(i4) == 2:
            name, langCode = i4[0], i4[1].split('_')[0]
            if langCode == 'zh':
                langCode = i4[1].lower().replace('_', '-')
        elif len(i4) == 3:
            name, langCode = ' '.join([i4[0], i4[1]]), i4[2].replace('_', '-').split('-')[0]
        else:
            raise Exception("Unexpected voice name found on Mac's say: ", i4)

        i4[0], i4[1] = langCode, name
        i4.append(combo)
        i4.append(examp)
        i3.append(i4)

    return i3


class Say(BaseSpeecher):
    # We want to call 'say -v ?' only once at runtime.
    # Don't call the command every time voice type changed.
    from gui.utils import isMac
    if isMac:
        # voiceCombo has voice names shown in a combobox on Preferences
        infos = getTtsHelp()
        code2Names = {key: {'Not Available': None} for key in LANGUAGES}

        for info in infos:
            if info[0] in code2Names:
                code2Names[info[0]][info[2]] = info[1]
                if 'Not Available' in code2Names[info[0]]:
                    del code2Names[info[0]]['Not Available']


    def dictate(self, script, langCode=None, output=None):
        print("Script: %s (%s)" % (script, langCode))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, output, langCode=langCode)
        else:
            call('say -v {name} "{script}"'.format(name=langCode, script=script), shell=True)

    def save(self, script, output, langCode=None):
        ppl = self.selectName(langCode)
        cmd = 'say %s "%s" -o %s.aiff;' \
              'ffmpeg -loglevel panic -i %s.aiff -ac 2 -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
              % (ppl, script, output, output, output)
        call(cmd, shell=True)

    def selectName(self, langCode):
        try:
            # Fixme: Allow users to select their favorite voice from a language
            # Currently we pick up the first voice from the list of them for a language
            ppl = '-v ' + self.code2Names[langCode][0]
        except (KeyError):
            ppl = ''
            print("Unsupported language detected: %s" % langCode)
        return ppl

    # Actually pre'listen' though.
    def preview(self, langCode, script='If any proper sample sentence is not found, I read this.'):
        self.dictate(script, langCode=langCode)
