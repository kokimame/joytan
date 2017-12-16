from emotan.speaker import *
from gui.utils import LANGUAGES


# TODO: Rename to 'getHelp' and Move to inside of Speaker class
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
            i4 = i4[0:2] # Unifying the length of i4 equal to 2
        else:
            raise Exception("Unexpected voice name found on Mac's say: ", i4)

        i4[0], i4[1] = langCode, name
        i4.append(combo)
        i4.append(examp)
        i3.append(i4)

    return i3


class Say(BaseSpeaker):
    # Call 'say -v ?' only once at runtime.

    from gui.utils import isMac
    if isMac:
        # voiceCombo has voice names shown in a combobox on Preferences
        infos = getTtsHelp()
        code2Vids = {key: {'Not Available': None} for key in LANGUAGES}
        vid2Combo = {}
        vid2examp = {}

        for info in infos:
            if info[0] in code2Vids:
                code2Vids[info[0]][info[2]] = info[1]
                vid2examp[info[1]] = info[3]
                if 'Not Available' in code2Vids[info[0]]:
                    del code2Vids[info[0]]['Not Available']


    def dictate(self, script, voiceId, output=None):
        print("Script: %s (%s)" % (script, voiceId))

        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            self.save(script, output, voiceId=voiceId)
        else:
            call('say -v {vid} "{script}"'.format(vid=voiceId, script=script), shell=True)

    def save(self, script, output, voiceId=None):
        cmd = 'say -v %s "%s" -o %s.aiff;' \
              'ffmpeg -loglevel panic -i %s.aiff -ac 2 -acodec libmp3lame -ar 44100 -ab 64k -f mp3 %s.mp3' \
              % (voiceId, script, output, output, output)
        call(cmd, shell=True)

    # Actually pre'listen' though.
    def preview(self, voiceId, script=None):
        if not script:
            script = self.vid2examp[voiceId]

        self.dictate(script, voiceId)
