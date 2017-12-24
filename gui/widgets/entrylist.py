from gui.qt import *


class EntryList(QListWidget):

    class Setting:
        def __init__(self):
            self.lv1 = 0  # This will be expanded soon at the 'reshape()' below!
            self.lv2 = 0  # Same here. The method is a little bit dumb.
            # Maps given Entry editor section to TTS service for dictation
            self.ttsmap = {'atop': None}

            self.reshape(lv1=1, lv2=1)

        def reshape(self, lv1=None, lv2=None):
            if lv1 and (self.lv1 != lv1):
                self.lv1 = lv1
                self._reshape()
            if lv2 and (self.lv2 != lv2):
                self.lv2 = lv2
                self._reshape()

        def _reshape(self):
            # Expand ttsmap and tags with default value
            for i in range(1, self.lv1 + 1):
                if 'def-%d' % i not in self.ttsmap:
                    self.ttsmap['def-%d' % i] = None
                for j in range(1, self.lv2 + 1):
                    if 'ex-%d-%d' % (i, j) not in self.ttsmap:
                        self.ttsmap['ex-%d-%d' % (i, j)] = None

        def is_voiceless(self):
            for key, val in self.ttsmap.items():
                # if TTS is not allocated
                if not val:
                    return True
            else:
                return False

        def _keys(self):
            # Sort and return keys to access the text of Entry's QLineEditor
            return sorted(self.ttsmap)

        # Returns a dictionary of EntryList properties. Will be called on saving the list.
        def data(self):
            data = {'lv1': self.lv1,
                    'lv2': self.lv2,
                    'ttsmap': self.ttsmap}
            return data

    def __init__(self, parent=None):
        super(EntryList, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)
        self.setting = self.Setting()

    def _new_entry(self, index, name, mode, setting):
        from gui.widgets.entry import EntryWidget
        eui, ew = QListWidgetItem(), EntryWidget(self, index, name, mode, setting)
        ew.move.connect(self._move_entry)
        ew.delete.connect(self._remove_at)
        eui.setSizeHint(ew.sizeHint())
        return eui, ew

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

    def update_entry(self, row, items):
        ew = self.get_entry_at(row)
        ew.update_editor(items)

    def add_entry(self, name, mode):
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

    def _remove_at(self, row):
        self.takeItem(row)
        self.update_all()

    def remove_selected(self):
        for ew in self.get_entry_selected():
            self.takeItem(ew.row)
            self._indexing()
        self.update_all()

    def remove_all(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def _indexing(self):
        # Update index of Entries after Nth Entry
        for i in range(self.count()):
            ew = self.get_entry_at(i)
            ew.update_index(i)

    def update_all(self):
        # Update the inside of the Entries
        for i in range(self.count()):
            eui = self.item(i)
            ew = self.itemWidget(eui)
            ew.update_index(i)
            ew.update_view()
            eui.setSizeHint(ew.sizeHint())
            ew.repaint()

        self.repaint()

    def update_mode(self, newMode):
        for ew in self.get_entry_all():
            ew.set_mode(newMode)

    def get_entry_selected(self):
        return [self.itemWidget(eui) for eui in self.selectedItems()]

    def get_entry_all(self):
        return [self.get_entry_at(i) for i in range(self.count())]

    def get_entry_at(self, row):
        return self.itemWidget(self.item(row))
