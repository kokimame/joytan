import json

import gui
from gui.utils import getFile


def on_open(mw):
    filter = "Emotan EntryList format (*.eel)"
    # Fixme: Read multiple files and adding their contents one by one to the list.
    try:
        file = getFile(mw, "Open exising Emotan EntryList", dir=mw.setting['workspace'], filter=filter)
    except:
        return

    if not file:
        print("Exception: File not found")
        return

    with open(file, 'r') as f:
        jd = json.loads(f.read())

    eset = jd[0]
    mw.entrylist.remove_all()
    mw.entrylist.setting.reshape(lv1=eset['lv1'], lv2=eset['lv2'])
    mw.entrylist.setting.ttsmap = eset['ttsmap']

    setting = mw.entrylist.setting.data()
    for data in jd[1:]:
        setting['lv1'] = data['lv1']
        setting['lv2'] = data['lv2']
        ew = mw.entrylist.add_entry(data['atop'], mw.mode)
        for i in range(0, ew.lv1):
            ew.editors['def-%d' % (i+1)].setText(data['def-%d' % (i+1)])
            for j in range(0, ew.lv2):
                ew.editors['ex-%d-%d' % (i+1, j+1)].setText(data['ex-%d-%d' % (i+1, j+1)])

    mw.entrylist.update_all()
