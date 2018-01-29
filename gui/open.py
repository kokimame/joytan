# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import csv
import json

import gui
from gui.utils import getFile

# TODO: Logic for opening csv should be moved to joytan/joytan,
# and in this directory we need to implement an open dialog to
# preview csv files and give options about which columns & rows to open.

def on_open(mw, file=None):
    filter = "CSV file for Joytan EntryList (*.csv)"
    if not file:
        try:
            file = getFile(mw, "Open Existing Joytan EntryList",
                           dir=mw.config['workspace'], filter=filter)
            if not file:
                return
        except:
            return

    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = remove_trash_row(next(reader))

        column = {}
        ndef, nex = 0, 0
        if validate_header(head):
            header = head
            for col in head:
                column[col] = []
            # Counting ndef & nex to reshape entrylist
            for key in header:
                if key == "atop":
                    continue
                ks = key.split('-')
                if len(ks) == 2:  # if key is def-n
                    ndef = max(int(ks[1]), ndef)
                elif len(ks) == 3:  # if key is ex-n-n
                    nex = max(int(ks[2]), nex)
                else:
                    raise Exception("Invalid key found %s. "
                                    "Header-validation is failing." % key)
        else:
            header = []
            for i in range(1, len(head) + 1):
                if i == 1:
                    column['atop'] = [head[i - 1]]
                    header.append('atop')
                elif (i + 8) % 10 == 0:
                    ndef = int((i + 8) / 10)
                    header.append('def-%d' % ndef)
                    column['def-%d' % ndef] = [head[i - 1]]
                else:
                    nex = i - 1 - ndef
                    header.append('ex-%d-%d' % (ndef, nex))
                    column['ex-%d-%d' % (ndef, nex)] = [head[i - 1]]

        mw.entrylist.set_config('reshape', dict(ndef=ndef, nex=nex))

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

def remove_trash_row(header):
    TRASH = ['']
    for tr in TRASH:
        if tr in header:
            header.remove(tr)
    return header

def validate_header(header):
    _valid_keys = ['atop']
    _valid_keys.extend(['def-%d' % i for i in range(1, 10)])
    _valid_keys.extend(['ex-%d-%d' % (i, j) for i in range(1, 10)
                                            for j in range(1, 10)])
    return (set(header) & set(_valid_keys)) == set(header)
