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
    # We want to call 'say -v ?' only once at runtime.
    # Don't call the command every time voice type changed.
    from gui.utils import isMac
    if isMac:
        # voiceCombo has voice names shown in a combobox on Preferences
        voiceInfo = getVoiceInfo()
        voiceCombo = voiceInfo.keys()
        code2Names = {}
        for vc in voiceCombo:
            vcs = vc.split(' ')
            if len(vcs) == 2:
                name, langCode = vcs[0], vcs[1].replace('_', '-').split('-')[0]
            elif len(vcs) == 3: # 2 words voice name such as 'Good News' and 'Pipe organ'.
                name, langCode = ' '.join([vcs[0], vcs[1]]), vcs[2].replace('_', '-').split('-')[0]
            else:
                raise Exception("Unexpected voice name found on Mac's say: ", vcs)

            try:
                code2Names[langCode].append(name)
            except KeyError:
                code2Names[langCode] = [name]
        print(code2Names)


    def dictate(self, script, langCode=None, output=None):
        print("Script: %s (%s)" % (script, langCode))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, output, langCode=langCode)

        else:
            ppl = self.selectName(langCode)
            call('say %s "%s"' % (ppl, script), shell=True)

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
    def preview(self, combo):
        script = self.voiceInfo[combo]
        combo = combo.split(' ')
        name = ' '.join(combo[0: len(combo) - 1])
        lang = combo[-1].split('_')
        call('say -v {name} "{script}"'.format(name=name, script=script), shell=True)
