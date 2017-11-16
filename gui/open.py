import json

import gui
from gui.utils import getFiles

def onOpen(mw):
    filter = "Emotan Wordlist format (*.ewl)"
    files = getFiles(mw, "Open exising Emotan Wordlist", dir=mw.pref['workspace'], filter=filter)

    if not files:
        print("Exception: File not found")
        return

    for file in files:
        openEwl(file)

    gui.dialogs.open("LangDetectDialog", mw)


def openEwl(file):
    with open(file, 'r') as f:
        jd = json.loads(f.read())
        for data in jd:
            print(data)