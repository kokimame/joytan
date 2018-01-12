import os
import csv

import gui
from gui.qt import *
from gui.utils import getFileToSave

def on_save(mw):
    # Save text stored in each of Entry as csv format (*.jel.csv).
    filter = "Joytan EntryList format (*.csv)"
    try:
        newfile = getFileToSave(mw, "Save Wordlist",
                                dir=mw.config['workspace'],
                                filter=filter,
                                suffix="jel.csv")
    except:
        return

    with open(newfile, "w") as f:
        cols = mw.entrylist.get_config('ewkeys')
        writer = csv.DictWriter(f, cols)
        writer.writeheader()

        for ew in mw.entrylist.get_entry_all():
            writer.writerow(ew.data())