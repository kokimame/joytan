# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import time
import csv

from gui.qt import *
from gui.utils import path_temp


class OpenCsvThread(QThread):

    new_entry = pyqtSignal(str, dict)
    reshape = pyqtSignal(dict)

    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def run(self):
        assert self.path

        with open(self.path, 'r', encoding='utf-8') as f:
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
                # If header is not specified by loaded csv file,
                # read first column as 'atop' and the others as 'def-n'
                nex = 0
                header = []
                for i in range(1, len(head) + 1):
                    if i == 1:
                        column['atop'] = [head[i - 1]]
                        header.append('atop')
                    else:
                        ndef = i - 1
                        header.append('def-%d' % ndef)
                        column['def-%d' % ndef] = [head[i - 1]]

            self.reshape.emit(dict(ndef=ndef, nex=nex))

            for row in reader:
                for h, v in zip(header, row):
                    column[h].append(v)

            for i, atop in enumerate(column['atop']):
                items = {}
                for ewkey in list(column.keys()):
                    if ewkey == 'atop':
                        continue
                    items[ewkey] = column[ewkey][i]
                self.new_entry.emit(atop, items)
                self.msleep(50)


def remove_trash_row(header):
    TRASH = ['']
    for tr in TRASH:
        if tr in header:
            header.remove(tr)
    return header

def validate_header(header):
    _valid_keys = ['atop']
    _valid_keys.extend(['def-%d' % i for i in range(1, 100)])
    _valid_keys.extend(['ex-%d-%d' % (i, j) for i in range(1, 100)
                                            for j in range(1, 100)])
    return (set(header) & set(_valid_keys)) == set(header)
