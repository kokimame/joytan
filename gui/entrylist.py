from gui.qt import *

class EntryList(QListWidget):

    class Setting:
        def __init__(self):
            # Fixme: ...................
            self.dpw = 0 # This will be expanded soon at the 'reshape()' below!
            self.epd = 0 # Same here. The method is a little bit dumb.
            # Fixme: Allow users to choose default language from preference
            # Temporally set English by default
            self.defaultLang = 'en'
            # This maps from line key of an entry to language code and Voice ID for its text
            self.langMap = {'atop': [self.defaultLang, None]}

            self.reshape(dpw=1, epd=1)


        # FIXME: Need a method to shrink this setting
        def reshape(self, dpw=None, epd=None):
            if dpw and (self.dpw != dpw):
                self.dpw = dpw
                self._reshape()
            if epd and (self.epd != epd):
                self.epd = epd
                self._reshape()

            print("EntrySetting: LangMap -> ", self.langMap)

        def _reshape(self):
            # Expand langMap and tags with default value
            for i in range(0, self.dpw):
                try:
                    self.langMap['def-%d' % (i + 1)]
                except KeyError:
                    self.langMap['def-%d' % (i + 1)] = [self.defaultLang, None]
                for j in range(0, self.epd):
                    try:
                        self.langMap['ex-%d-%d' % (i + 1, j + 1)]
                    except KeyError:
                        self.langMap['ex-%d-%d' % (i + 1, j + 1)] = [self.defaultLang, None]

        def isVoiceless(self):
            for item, map in self.langMap.items():
                # Voice id is still None
                if not map[1]:
                    return True
            else:
                return False

        # Returns EntryList properties in a dictionary. Will be called on saving the list.
        def data(self):
            data = {'dpw': self.dpw,
                    'epd': self.epd,
                    'langMap': None}
            langMap = {'atop': self.langMap['atop']}

            for i in range(0, self.dpw):
                langMap['def-%d' % (i + 1)] = self.langMap['def-%d' % (i + 1)]
                for j in range(0, self.epd):
                    langMap['ex-%d-%d' % (i + 1, j + 1)] = self.langMap['ex-%d-%d' % (i + 1, j + 1)]

            data['langMap'] = langMap
            return data

    def __init__(self, parent=None):
        super(EntryList, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)
        self.setting = self.Setting()

    def initEntry(self, index, name, mode, setting, parent=None):
        from gui.entry import EntryWidget
        eui, ew = QListWidgetItem(), EntryWidget(index, name, mode, setting, parent=parent)
        eui.setSizeHint(ew.sizeHint())
        return eui, ew


    def updateEntry(self, name, items):
        for ew in self.getEntries():
            if ew.editors['atop'].text() == name:
                ew.updateEditors(items)
                return
        raise Exception("Error: Entry with atop '%s' is not found in the list" % name)

    def addEntry(self, name, mode, setting=None):
        if not setting:
            setting = self.setting.data()

        if name == '':
            pass
        elif name in [ew.editors['atop'] for ew in self.getEntries()]:
            print("Entry with atop %s already exists." % name)
            return

        eui, ew = self.initEntry(self.count() + 1, name, mode, setting, parent=self)

        self.addItem(eui)
        self.setItemWidget(eui, ew)

    def deleteSelected(self):
        for eui in self.selectedItems():
            ew = self.itemWidget(eui)
            self.takeItem(ew.index - 1)
            self.updateIndex()
        self.updateAll()

    def deleteAll(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def updateIndex(self):
        # Update index of Entries after Nth Entry
        for i in range(self.count()):
            ew = self.getByIndex(i)
            ew.index = i + 1

    def updateAll(self):
        # Update the inside of the Entries in the list
        print("Entry updates")
        for i in range(self.count()):
            eui = self.item(i)
            ew = self.itemWidget(eui)
            ew.index = i + 1
            ew.updateView()
            eui.setSizeHint(ew.sizeHint())

        self.repaint()

    def updateMode(self, newMode):
        for ew in self.getEntries():
            ew.setMode(newMode)

    def getEntries(self):
        return [self.getByIndex(i) for i in range(self.count())]

    def getByName(self, name):
        for ew in self.getEntries():
            if ew.editors['atop'].text() == name:
                return ew
        raise Exception("Error: Entry with atop '%s' is not found in the list" % name)

    def getByIndex(self, index):
        return self.itemWidget(self.item(index))
