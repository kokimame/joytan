import json

import gui
from gui.utils import getFile


def on_open(mw, file=None):
    filter = "Joytan EntryList format (*.jel)"
    # Fixme: Read multiple files and adding their contents one by one to the list.
    if not file:
        try:
            file = getFile(mw, "Open exising Joytan EntryList",
                           dir=mw.config['workspace'], filter=filter)
        except:
            return

    if not file:
        print("Exception: File not found")
        return

    with open(file, 'r') as f:
        jd = json.loads(f.read())

    config = jd[0]
    mw.entrylist.remove_all()
    mw.entrylist.set_config('reshape', dict(lv1=config['lv1'], lv2=config['lv2']))
    mw.entrylist.set_config('ttsmap', config['ttsmap'])

    for data in jd[1:]:
        ew = mw.entrylist.add_entry(data['atop'], mw.mode)
        for i in range(0, ew.lv1):
            ew.editors['def-%d' % (i+1)].setText(data['def-%d' % (i+1)])
            for j in range(0, ew.lv2):
                ew.editors['ex-%d-%d' % (i+1, j+1)].setText(data['ex-%d-%d' % (i+1, j+1)])

    mw.entrylist.update_all()
