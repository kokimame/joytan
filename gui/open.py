import json

import gui
from gui.utils import getFile

def onOpen(mw):
    filter = "Emotan Wordlist format (*.ewl)"
    # Fixme: Read multiple files and adding their contents one by one to the list.
    file = getFile(mw, "Open exising Emotan Wordlist", dir=mw.pref['workspace'], filter=filter)

    if not file:
        print("Exception: File not found")
        return


    with open(file, 'r') as f:
        jd = json.loads(f.read())

    eset = jd[0]
    mw.entrylist.deleteAllEntries()
    mw.entrylist.setting.expand(dpw=eset['dpw'])
    mw.entrylist.setting.expand(epd=eset['epd'])
    mw.entrylist.setting.langMap = eset['langMap']

    setting = mw.entrylist.setting.data()
    for data in jd[1:]:
        setting['dpw'] = data['dpw']
        setting['epd'] = data['epd']
        mw.entrylist.addEntry(data['name'], mw.entryMode)
        ew = mw.entrylist.getEntry(data['name'])
        for i in range(0, ew.dpw):
            ew.editors['def-%d' % (i+1)].setText(data['def-%d' % (i+1)])
            for j in range(0, ew.epd):
                ew.editors['ex-%d-%d' % (i+1, j+1)].setText(data['ex-%d-%d' % (i+1, j+1)])

    mw.entrylist._update()
