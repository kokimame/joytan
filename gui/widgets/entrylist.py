import re
from gui.qt import *


class EntryList(QListWidget):

    class Setting(QWidget):

        shape = pyqtSignal()

        def __init__(self):
            super().__init__()
            self.lv1 = 0  # This will be expanded soon at the 'reshape()' below!
            self.lv2 = 0  # Same here. The method is a little bit dumb.
            # Maps given Entry editor section to TTS service for dictation
            self.ttsmap = {'atop': None}
            self.reshape(lv1=1, lv2=0)

        def reshape(self, lv1=None, lv2=None):
            if self.lv1 != (lv1 or None) or self.lv2 != (lv2 or None):
                self.lv1 = lv1
                self.lv2 = lv2
                self._reshape()
                self.shape.emit()

        def _reshape(self):
            avail_keys = ['atop']

            # Expand ttsmap and tags with default value
            for i in range(1, self.lv1 + 1):
                ewkey = 'def-%d' % i
                avail_keys.append(ewkey)
                if ewkey not in self.ttsmap:
                    self.ttsmap[ewkey] = None
                for j in range(1, self.lv2 + 1):
                    ewkey = 'ex-%d-%d' % (i, j)
                    avail_keys.append(ewkey)
                    if ewkey not in self.ttsmap:
                        self.ttsmap[ewkey] = None
            # Exclude keys out of size of levels from ttsmap
            keys = list(self.ttsmap.keys())
            for ewkey in keys:
                if ewkey not in avail_keys:
                    self.ttsmap.pop(ewkey, None)


        def is_voiceless(self):
            for key, val in self.ttsmap.items():
                # if TTS is not allocated
                if not val:
                    return True
            else:
                return False

        def ewkeys(self):
            # Sort ewkeys in the same order shown in Edit mode on EntryWidget
            ewkeys = ['atop']
            for i in range(1, self.lv1 + 1):
                ewkeys.append('def-%d' % i)
                for j in range(1, self.lv2 + 1):
                    ewkeys.append("ex-%d-%d" % (i, j))

            return ewkeys

        # Returns a dictionary of EntryList properties. Will be called on saving the list.
        def data(self):
            data = {'lv1': self.lv1,
                    'lv2': self.lv2,
                    'ttsmap': self.ttsmap}
            return data

    def __init__(self, mw):
        super(EntryList, self).__init__()
        self.mw = mw
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setAcceptDrops(True)
        self.scrollToItem(self.currentItem())
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)
        self.setting = self.Setting()
        self.setting.shape.connect(lambda: self.update_all(reshape=True))
        self.initial_help = True
        self.addItem(QListWidgetItem("\nDrag text (only available for English) \n"
                                     "or Use Tools/Extract...\n"
                                     "or push (+) button bellow\n"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.clearSelection()

    def dragMoveEvent(self, event):
        # dropEvent doesn't get called without this overwritten method for some reason
        pass

    def dropEvent(self, event):
        # TODO
        # Very simple word extraction from English text only.
        # Later, extract dialog will get upgraded and called from here
        # for detailed option, such as language detection and char limits
        for word in re.compile('\w+').findall(event.mimeData().text()):
            if len(word) <= 2:
                continue
            self.add_entry(word, self.mw.mode)

    def count(self):
        if self.initial_help:
            return super().count() - 1
        else:
            return super().count()

    def _new_entry(self, index, name, mode, setting):
        from gui.widgets.entry import EntryWidget
        eui, ew = QListWidgetItem(), EntryWidget(self, index, name, mode, setting)
        ew.move.connect(self._move_entry)
        ew.delete.connect(self._remove_at)
        eui.setSizeHint(ew.sizeHint())
        return eui, ew

    def add_entry(self, name, mode):
        if self.initial_help:
            self.takeItem(0)
            self.initial_help = False
        if name == '':
            pass
        elif name in [ew.editors['atop'] for ew in self.get_entry_all()]:
            print("Entry with atop %s already exists." % name)
            return

        eui, ew = self._new_entry(self.count(), name, mode, self.setting.data())

        self.addItem(eui)
        self.setItemWidget(eui, ew)
        # Convenient to modify ew after adding it
        return ew

    def update_all(self, reshape=False):
        # Update the inside of the Entries
        for i in range(self.count()):
            eui = self.item(i)
            ew = self.itemWidget(eui)
            ew.update_index(i)
            if reshape:
                ew.reshape(self.setting.lv1, self.setting.lv2)
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
            ew.update_index(i)

    def _move_entry(self, now, next):
        """
        :param now: Row of the entry to move
        :param next: Row to which the entry moves
        ============
        Move EntryWidget by taking it from and inserting it to the list
        """
        old_ew = self.get_entry_at(now)
        eui = QListWidgetItem()
        eui.setSizeHint(old_ew.sizeHint())

        # Entry goes up
        if next > old_ew.row:
            to_insert = next + 1
            to_take = old_ew.row
        # Entry goes down
        else:
            to_insert = next
            to_take = old_ew.row + 1

        self.insertItem(to_insert, eui)
        self.setItemWidget(eui, old_ew)
        self.takeItem(to_take)
        self.update_all()

    def get_entry_at(self, row):
        return self.itemWidget(self.item(row))

    def get_entry_all(self):
        return [self.get_entry_at(i) for i in range(self.count())]

    def get_entry_selected(self):
        return [self.itemWidget(eui) for eui in self.selectedItems()]

    def _remove_at(self, row):
        self.takeItem(row)
        self.update_all()

    def remove_all(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def remove_selected(self):
        for ew in self.get_entry_selected():
            self.takeItem(ew.row)
            self._indexing()
        self.update_all()
