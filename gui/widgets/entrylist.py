# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import re
from gui.qt import *


class EntryList(QListWidget):

    class _Configuration(QWidget):

        shape = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.ndef = 0  # This will be expanded soon at the 'reshape()' below!
            self.nex = 0  # Same here. The method is a little bit dumb.
            # Maps given Entry editor section to TTS service for dictation
            self.ttsmap = {'atop': None}
            self.reshape(ndef=1, nex=0)

        def reshape(self, ndef=None, nex=None):
            if self.ndef != (ndef or None) or self.nex != (nex or None):
                self.ndef = ndef
                self.nex = nex
                self._reshape()
                self.shape.emit()

        def _reshape(self):
            avail_keys = ['atop']

            # Expand ttsmap and tags with default value
            for i in range(1, self.ndef + 1):
                ewkey = 'def-%d' % i
                avail_keys.append(ewkey)
                if ewkey not in self.ttsmap:
                    self.ttsmap[ewkey] = None
                for j in range(1, self.nex + 1):
                    ewkey = 'ex-%d-%d' % (i, j)
                    avail_keys.append(ewkey)
                    if ewkey not in self.ttsmap:
                        self.ttsmap[ewkey] = None
            # Exclude keys out of size of levels from ttsmap
            keys = list(self.ttsmap.keys())
            for ewkey in keys:
                if ewkey not in avail_keys:
                    self.ttsmap.pop(ewkey, None)

        def keys_undefined(self):
            # Return ewkeys to which TTS service undefined
            undefs = []
            for key, val in self.ttsmap.items():
                # if TTS is not allocated
                if not val:
                    undefs.append(key)
            return undefs

        def ewkeys(self):
            # Sort and return ewkeys in the same order shown in Edit mode of EntryWidget
            ewkeys = ['atop']
            for i in range(1, self.ndef + 1):
                ewkeys.append('def-%d' % i)
                for j in range(1, self.nex + 1):
                    ewkeys.append("ex-%d-%d" % (i, j))

            return ewkeys

        # Returns a dictionary of EntryList properties. Will be called on saving the list.
        def data(self):
            data = {'ndef': self.ndef,
                    'nex': self.nex,
                    'ttsmap': self.ttsmap}
            return data

    # A snippet displayed in EntryList every time the app are started
    _STARTER_MESSAGE = """
 Hi! Thank you for using Joytan!
 To start creating audio/textbooks...
 Drag text here (this only works properly for English)
 or push (+) button below and type by yourself.
 After bringing everything you need,
 hit the button [-> Audio] or [-> Text]!
 Tips: You can drag entries to reorder them.   
    """

    def __init__(self, mw):
        super(EntryList, self).__init__()
        self.mw = mw
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDropIndicatorShown(True)
        self.setAutoScroll(True)
        self.scrollToItem(self.currentItem())
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid gray; 
                                                border-top: 1px solid gray;}
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)

        self.config = self._Configuration()
        self.config.shape.connect(lambda: self.update_all(reshape=True))

        self._has_starter_help = True
        _starter_label = QLabel(self._STARTER_MESSAGE)

        _starter_label.setStyleSheet("QLabel { color : green; }")
        lwi = QListWidgetItem()
        lwi.setSizeHint(_starter_label.sizeHint())
        self.addItem(lwi)
        self.setItemWidget(lwi, _starter_label)

    def mouseDoubleClickEvent(self, event):
        self.clearSelection()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            super().mousePressEvent(event)
            self._click_menu()
        elif event.button() == Qt.LeftButton:
            super().mousePressEvent(event)

    def _click_menu(self):
        m = QMenu(self.mw)
        a = m.addAction("Delete Selected Items")
        a.triggered.connect(self.remove_selected)
        if self._has_starter_help:
            a.setDisabled(True)
        above = m.addAction("Insert Item Above")
        below = m.addAction("Insert Item Below")
        above.triggered.connect(lambda: self._insert_entry())
        below.triggered.connect(lambda: self._insert_entry(above=False))
        if len(self.selectedItems()) != 1 or self._has_starter_help:
            above.setDisabled(True)
            below.setDisabled(True)
        m.exec_(QCursor.pos())

    def dragEnterEvent(self, event):
        # Dragging plain text (wishing it's written in English) -> accept
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        # Dragging QListWidgetItem -> accept
        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.accept()

    def dragMoveEvent(self, event):
        # dropEvent gets ignored without overwriting this method for some reason
        # The super triggers autoScrolling.
        super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            # TODO
            # Very simple word extraction only available for  English text.
            # Later, extract dialog will get upgraded and called from here.
            # Then set detailed option, such as language detection and char limits
            for word in re.compile('\w+').findall(event.mimeData().text()):
                if len(word) <= 2:
                    continue
                self.add_entry(atop=word, duplicate=False)
        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            # Call internal move
            super().dropEvent(event)
            self._indexing()

    def count(self):
        if self._has_starter_help:
            return super().count() - 1
        else:
            return super().count()

    def _new_entry(self, name, mode):
        from gui.widgets.entry import EntryWidget

        levels = (self.config.ndef, self.config.nex)
        eui, ew = QListWidgetItem(), EntryWidget(name, mode, self.count(), levels)
        ew.move.connect(self._move_entry)
        ew.delete.connect(self._remove_entry_at)
        eui.setSizeHint(ew.sizeHint())
        return eui, ew

    def add_entry(self, atop='', duplicate=True):
        if self._has_starter_help:
            self.takeItem(0)
            self._has_starter_help = False
        if not duplicate:
            # If Entry with the new name already exists
            for ew in self.get_entry_all():
                if atop == ew['atop']:
                    return

        eui, ew = self._new_entry(atop, self.mw.mode)

        self.addItem(eui)
        self.setItemWidget(eui, ew)
        # Convenient to modify ew after adding it
        return ew

    def _insert_entry(self, above=True):
        assert len(self.selectedItems()) == 1
        ew = self.add_entry()

        selected = self.get_entry_selected()[0]
        if above:
            ew.move_to(selected.row)
        else:
            ew.move_to(selected.row + 1)

    def update_all(self, reshape=False):
        # Update the inside of the Entries
        for i in range(self.count()):
            eui = self.item(i)
            ew = self.itemWidget(eui)
            ew.row = i
            if reshape:
                ew.reshape(self.config.ndef, self.config.nex)
            ew.update_view()
            eui.setSizeHint(ew.sizeHint())
            ew.repaint()
        self.repaint()

    def update_entry(self, row, items):
        ew = self.get_entry_at(row)
        ew.update_editor(items)

    def update_mode(self, newMode):
        for ew in self.get_entry_all():
            ew.set_mode(newMode)

    def _indexing(self):
        # Update index of Entries after Nth Entry
        for i in range(self.count()):
            ew = self.get_entry_at(i)
            ew.row = i
            ew.update_view()

    def _move_entry(self, now, next_row, to_update):
        """
        :param now: Row of the target entry to move
        :param next_row: Row to which the entry moves
        :param to_update: Update the listwidget if True (True by default)
        
        Move EntryWidget by taking it from and inserting it back to the EntryList
        """
        # Check destination in the list
        if not 0 <= next_row < self.count():
            return

        old_ew = self.get_entry_at(now)
        eui = QListWidgetItem()
        eui.setSizeHint(old_ew.sizeHint())

        # Entry goes up
        if next_row > old_ew.row:
            to_insert = next_row + 1
            to_take = old_ew.row
        # Entry goes down
        else:
            to_insert = next_row
            to_take = old_ew.row + 1

        self.insertItem(to_insert, eui)
        self.setItemWidget(eui, old_ew)
        self.takeItem(to_take)

        if to_update:
            self.update_all()
        else:
            # TODO: Most of part duplicated with _indexing
            for i, ew in enumerate(self.get_entry_all()):
                ew.row = i

    def get_entry_at(self, row):
        return self.itemWidget(self.item(row))

    def get_entry_all(self):
        return [self.get_entry_at(i) for i in range(self.count())]

    def get_entry_selected(self):
        return [self.itemWidget(eui) for eui in self.selectedItems()]

    def _remove_entry_at(self, row):
        self.takeItem(row)
        self.update_all()

    def remove_entry_all(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def get_config(self, key):
        if key == 'ewkeys':
            return self.config.ewkeys()
        if key == 'undefined':
            return self.config.keys_undefined()
        if key == 'ttsmap':
            return self.config.ttsmap
        if key == 'ndef':
            return self.config.ndef
        if key == 'nex':
            return self.config.nex
        if key == 'data':
            return self.config.data()

        try:
            tts = self.config.ttsmap[key]
            return tts
        except KeyError:
            raise Exception("Unknown key: %s" % key)


    def set_config(self, key, new):
        if key == 'reshape':
            self.config.reshape(**new)
            return
        if key == 'ttsmap':
            self.config.ttsmap = new
            return

        try:
            self.config.ttsmap[key] = new
        except KeyError:
            raise Exception("Unknown key: %s" % key)

    def remove_selected(self):
        if self._has_starter_help:
            return

        for ew in self.get_entry_selected():
            self.takeItem(ew.row)
            self._indexing()
        self.update_all()
