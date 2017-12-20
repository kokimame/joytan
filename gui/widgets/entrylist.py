from gui.qt import *

class EntryList(QListWidget):

    class Setting:
        def __init__(self):
            # Fixme: ...................
            self.lv1 = 0 # This will be expanded soon at the 'reshape()' below!
            self.lv2 = 0 # Same here. The method is a little bit dumb.
            # Maps given Entry editor section to TTS service for dictation
            self.ttsMap = {'atop': None}

            self.reshape(lv1=1, lv2=1)

        def reshape(self, lv1=None, lv2=None):
            if lv1 and (self.lv1 != lv1):
                self.lv1 = lv1
                self._reshape()
            if lv2 and (self.lv2 != lv2):
                self.lv2 = lv2
                self._reshape()

        def _reshape(self):
            # Expand ttsMap and tags with default value
            for i in range(1, self.lv1 + 1):
                if 'def-%d' % i not in self.ttsMap:
                    self.ttsMap['def-%d' % i] = None
                for j in range(1, self.lv2 + 1):
                    if 'ex-%d-%d' % (i, j) not in self.ttsMap:
                        self.ttsMap['ex-%d-%d' % (i, j)] = None

        def isVoiceless(self):
            for key, val in self.ttsMap.items():
                # if TTS is not allocated
                if not val:
                    return True
            else:
                return False

        # Returns EntryList properties in a dictionary. Will be called on saving the list.
        def data(self):
            data = {'lv1': self.lv1,
                    'lv2': self.lv2,
                    'ttsMap': None}
            ttsMap = {'atop': self.ttsMap['atop']}

            for i in range(1, self.lv1 + 1):
                ttsMap['def-%d' % i] = self.ttsMap['def-%d' % i]
                for j in range(1, self.lv2 + 1):
                    ttsMap['ex-%d-%d' % (i, j)] = self.ttsMap['ex-%d-%d' % (i, j)]

            data['ttsMap'] = ttsMap
            return data

    def __init__(self, parent=None):
        super(EntryList, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)
        self.setting = self.Setting()

    def initEntry(self, index, name, mode, setting):
        from gui.widgets.entry import EntryWidget
        eui, ew = QListWidgetItem(), EntryWidget(self, index, name, mode, setting)
        ew.move.connect(self._move_entry)
        ew.delete.connect(self.delete_at)
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
        self.updateAll()
        #self._debug()

    def _debug(self):
        print("count: %d" % self.count())
        for i in range(self.count()):
            eui = self.item(i)
            ew = self.itemWidget(eui)
            print("Type (eui/ew): ", type(eui), type(ew))
            print("ew atop/index:", ew.atop, ew.row + 1)


    def updateEntry(self, row, items):
        ew = self.get_entry_at(row)
        ew.updateEditors(items)

    def addEntry(self, name, mode):
        if name == '':
            pass
        elif name in [ew.editors['atop'] for ew in self.getEntries()]:
            print("Entry with atop %s already exists." % name)
            return

        eui, ew = self.initEntry(self.count(), name, mode, self.setting.data())

        self.addItem(eui)
        self.setItemWidget(eui, ew)

    def delete_at(self, row):
        self.takeItem(row)
        self.updateAll()

    def deleteSelected(self):
        for eui in self.selectedItems():
            ew = self.itemWidget(eui)
            self.takeItem(ew.row)
            self.updateIndex()
        self.updateAll()

    def deleteAll(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def updateIndex(self):
        # Update index of Entries after Nth Entry
        for i in range(self.count()):
            ew = self.get_entry_at(i)
            ew.update_index(i)

    def updateAll(self):
        # Update the inside of the Entries
        for i in range(self.count()):
            eui = self.item(i)
            ew = self.itemWidget(eui)
            ew.update_index(i)
            ew.updateView()
            eui.setSizeHint(ew.sizeHint())
            ew.repaint()

        self.repaint()

    def updateMode(self, newMode):
        for ew in self.getEntries():
            ew.setMode(newMode)

    def getEntries(self):
        return [self.get_entry_at(i) for i in range(self.count())]

    # FIXME: To remove. Only get entries by index
    def getByName(self, name):
        for ew in self.getEntries():
            if ew.editors['atop'].text() == name:
                return ew
        raise Exception("Error: Entry with atop '%s' is not found in the list" % name)

    # FIXME: Function name is unclear about what to get, i.e, EntryWidget.
    # Like entry_at(int)
    def get_entry_at(self, row):
        return self.itemWidget(self.item(row))
