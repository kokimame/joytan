import gui
from gui.qt import *
from gui.utils import saveFile

def onSave(mw):
    filter = "Emotan Wordlist format (*.emt)"
    saveFile(mw, "Save Wordlist", dir=mw.pref['workspace'], filter=filter)