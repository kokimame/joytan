import os
import json

import gui
from gui.qt import *
from gui.utils import getFileToSave

def onSave(mw):
    # Save contents of framelist as a file, temporally whose extension is original '.emt'.
    filter = "Emotan Wordlist format (*.ewl)"
    newfile = getFileToSave(mw, "Save Wordlist", dir=mw.pref['workspace'], filter=filter)

    # Ignore if selected file is a directory by accident
    if os.path.isdir(newfile):
        return

    maxb = mw.framelist.maxBundle
    with open(newfile, "w") as f:
        f.write("[dpw]%d\n" % maxb.dpw)
        f.write("[epd]%d\n" % maxb.epd)

        f.write("[name]%s\n" % maxb.langMap['name'])
        for i in range(0, maxb.dpw):
            f.write("[def-%d]%s\n" % (i+1, maxb.langMap['def-%d' % (i+1)]))
            for j in range(0, maxb.epd):
                f.write("[ex-%d-%d]%s\n" % (i+1, j+1, maxb.langMap['ex-%d-%d' % (i+1, j+1)]))

        f.write("\n[contents]\n")

        for bw in mw.framelist.getCurrentBundleWidgets():
            json.dump(bw.dataToSave(), f, indent=4)