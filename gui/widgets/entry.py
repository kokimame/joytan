# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GNU version 3 or later; http://www.gnu.org/licenses/gpl.html


from gui.qt import *


class Editor(QWidget):
    _ITALIC = QFont()
    _ITALIC.setItalic(True)

    COLOR = {'atop': "background-color : rgb(%d,%d,%d)" % (255,255,180),
             'def': "background-color : rgb(%d,%d,%d)" % (255,180,230),
             'ex': "background-color : rgb(%d,%d,%d)" % (180,230,255),}

    def __init__(self, ewkey, text=""):
        super(Editor, self).__init__()
        self.ewkey = ewkey
        self.label = QLabel(ewkey)
        self.label.setFixedWidth(40)
        self.label.setFont(self._ITALIC)
        self.label.setStyleSheet(self._color(ewkey))
        self.editor = QLineEdit(text)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def _color(self, ewkey):
        sk = ewkey.split('-')
        if 'atop' in sk:
            return self.COLOR['atop']
        elif 'def' in sk:
            return self.COLOR['def']
        elif 'ex' in sk:
            return self.COLOR['ex']
        else:
            raise Exception("Wrong ewkey")

    # The function name is camel case as the class had to overwrite QLineEdit
    # otherwise too many rename were required.
    def setText(self, text):
        self.editor.setText(text)

    def text(self):
        return self.editor.text()


class EntryWidget(QWidget):
    # Design of QLabel shown on 'View' mode
    _ENTRY_VIEW = '<html><head/><body>{content}</body></html>'
    _FONT_ATOP = '<p><span style=" font-size:16pt; font-weight:520;">{index}. {text}</span></p>'
    _FONT_DEF = '<p>{num}. {text}</p>'
    _FONT_EX = '<p><span style="color:#8d8d8d;">&quot;{text}&quot;</span></p>'

    _BOLD, _ITALIC = QFont(), QFont()
    _BOLD.setBold(True)
    _ITALIC.setItalic(True)

    move = pyqtSignal(int, int)
    delete = pyqtSignal(int)

    def __init__(self, atop, mode, index, levels):
        super(EntryWidget, self).__init__()
        # 'View' or 'Edit' mode
        self.mode = mode
        # New Entry will be append to the end of the entrylist
        self.row = index
        # Entry setting
        self.ndef = levels[0]
        self.nex = levels[1]

        # Dictionary of QLineEdit.
        # Text stored in the editors will be the actual learning materials.
        # The keys, referenced as 'ewkey', come in 'atop', 'def-n', 'ex-n-n' where 0 < n < 10
        # ===
        # 'atop' : The name of Entry. Should be identical in the entrylist
        # 'def-x' : Main part of an Entry. Each entry has upto 9 of this section.
        # 'ex-x-x' : Sub part. Each 'def-x' has upto 9 of the sub section.
        # ===
        # NOTE: The name of keys must not be modified because we alphabetically sort them out in a process
        self.editors = {}

        # Building UI
        layout = QStackedLayout()
        layout.addWidget(self._ui_view(atop))
        layout.addWidget(self._ui_editor(atop=atop))
        self.setLayout(layout)
        self.set_mode(mode)

    def set_mode(self, new_mode):
        if new_mode == "View":
            self.layout().setCurrentIndex(0)
            self.mode = new_mode
        if new_mode == "Edit":
            self.layout().setCurrentIndex(1)
            self.mode = new_mode

    def _ui_view(self, atop):
        view = QLabel()
        view.setWordWrap(True)
        view.setObjectName("view")

        if atop == '':
            atop = "Unnamed Entry"

        view.setText(self._ENTRY_VIEW.format
                     (content=self._FONT_ATOP.format(index=self.row + 1, text=atop)))
        layout = QHBoxLayout()
        layout.addWidget(view)
        base = QWidget()
        base.setLayout(layout)

        # The base widget shown in View mode is always disabled for dragging,
        # but we want to make it look as if it's enabled, not dead-gray color!
        base.setDisabled(True)
        base.setStyleSheet(":disabled { color: #000000; }")
        return base

    def _ui_editor(self, atop=None):
        # Widget shown on Editor mode of EntryList
        layout = QVBoxLayout()

        if atop != None:
            self.editors['atop'] = Editor('atop', text=atop)
        layout.addWidget(self.editors['atop'])
        row = 1
        for i in range(1, self.ndef + 1):
            ewkey = 'def-%d' % i
            if ewkey not in self.editors:
                self.editors[ewkey] = Editor(ewkey)
            layout.addWidget(self.editors[ewkey])
            for j in range(1, self.nex + 1):
                ewkey = "ex-%d-%d" % (i, j)
                if ewkey not in self.editors:
                    self.editors[ewkey] = Editor(ewkey)
                layout.addWidget(self.editors[ewkey])
                row += 1
            row += 1

        base = QWidget()
        base.setLayout(layout)
        return base

    def reshape(self, ndef, nex):
        self.ndef, self.nex = ndef, nex
        stacked = self.layout()
        assert stacked
        # Old editor widget
        wig = stacked.widget(1)
        stacked.removeWidget(wig)
        stacked.addWidget(self._ui_editor())
        stacked.widget(0).repaint()
        stacked.widget(1).repaint()
        self.set_mode(self.mode)

    def update_view(self):
        atop = self['atop'] or "Unnamed Entry"
        content = self._FONT_ATOP.format(index=self.row + 1, text=atop)

        for i in range(1, self.ndef + 1):
            if self['def-%d' % i] != '':
                content += self._FONT_DEF.format(num=i, text=self['def-%d' % i])
            for j in range(1, self.nex + 1):
                if self['ex-%d-%d' % (i, j)] != '':
                    content += self._FONT_EX.format(text=self['ex-%d-%d' % (i, j)])

        view = self.findChild(QLabel, "view")
        view.setText(self._ENTRY_VIEW.format(content=content))

    # Set the text of downloaded contents to each of matched editors
    def update_editor(self, items):
        if 'atop' in items:
            self['atop'] = items['atop']

        for i in range(1, self.ndef + 1):
            if 'def-%d' % i in items:
                self['def-%d' % i] = items['def-%d' % i]
            for j in range(1, self.nex + 1):
                if 'ex-%d-%d' % (i, j) in items:
                    self['ex-%d-%d' % (i, j)] = items['ex-%d-%d' % (i, j)]

    def move_to(self, next):
        self.move.emit(self.row, next)

    def str_index(self):
        # Return string number from 00000 to 99999 based on the index
        index = self.row + 1
        snum = (5 - len(str(index))) * '0' + str(index)
        return snum

    # Returns the class' properties in a dictionary. Will be called on saving.
    def data(self):
        data = {}
        data['atop'] = self['atop']
        for i in range(1, self.ndef + 1):
            data['def-%d' % i] = self['def-%d' % i]
            for j in range(1, self.nex + 1):
                data['ex-%d-%d' % (i, j)] = self['ex-%d-%d' % (i, j)]

        return data

    def __getitem__(self, key):
        """
        Retrieve text stored in editors['ewkey'] using the ew[key] syntax 
        """
        try:
            return self.editors[key].text()
        except KeyError:
            raise KeyError("'%s' is not a valid ewkey ('EntryWidget Key')." % key)


    def __setitem__(self, key, text):
        """
        Set text to the specified editors['ewkey'] by ew[key] = text syntax
        """
        try:
            self.editors[key].setText(text)
        except KeyError:
            raise KeyError("'%s' is not a valid ewkey ('EntryWidget Key')." % key)


