import os
import json

import gui
from gui.qt import *
from gui.utils import getFileToSave


def on_save(mw):
    # Save contents of entrylist as a file, temporally whose extension is original '.jel'.
    filter = "Joytan EntryList format (*.jel)"
    try:
        newfile = getFileToSave(mw, "Save Wordlist", dir=mw.config['workspace'], filter=filter)
    except:
        return

    saving_data = []
    with open(newfile, "w") as f:
        saving_data.append(mw.entrylist.get_config('data'))

        for ew in mw.entrylist.get_entry_all():
            saving_data.append(ew.data())

        json.dump(saving_data, f, indent=4)
