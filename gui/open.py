import csv
import json

import gui
from gui.utils import getFile


def on_open(mw, file=None):
    filter = "CSV file for Joytan EntryList (*.jel.csv)"
    if not file:
        try:
            file = getFile(mw, "Open Existing Joytan EntryList",
                           dir=mw.config['workspace'], filter=filter)
            if not file:
                return
        except:
            return

    with open(file, 'r') as f:
        reader = csv.reader(f)
        head = next(reader)

        # TODO:
        # if len(head) > 81, it's too large for Joytan
        # Do something

        column = {}
        if validate_header(head):
            header = head
            for col in head:
                column[col] = []
        else:
            ndef, nex = 0, 0
            header = []
            for i in range(1, len(head) + 1):
                if i == 1:
                    column['atop'] = [head[i - 1]]
                    header.append('atop')
                elif (i + 8) % 10 == 0:
                    ndef = (i + 8) / 10
                    header.append('def-%d' % ndef)
                    column['def-%d' % ndef] = [head[i - 1]]
                else:
                    nex = i - 1 - ndef
                    header.append('ex-%d-%d' % (ndef, nex))
                    column['ex-%d-%d' % (ndef, nex)] = [head[i - 1]]

        for row in reader:
            for h, v in zip(header, row):
                column[h].append(v)

        for i, atop in enumerate(column['atop']):
            ew = mw.entrylist.add_entry(atop=atop)
            items = {}
            for ewkey in list(column.keys()):
                if ewkey == 'atop':
                    continue
                items[ewkey] = column[ewkey][i]
            ew.update_editor(items)

        mw.entrylist.update_all()


def validate_header(header):
    _valid_keys = ['atop']
    _valid_keys.extend(['def-%d' % i for i in range(1, 10)])
    _valid_keys.extend(['ex-%d-%d' % (i, j) for i in range(1, 10)
                                            for j in range(1, 10)])

    return (set(header) & set(_valid_keys)) == set(header)
