from gui.qt import *

class EntryList(QListWidget):

    class Setting:
        def __init__(self):
            # Fixme: ...................
            self.lv1 = 0 # This will be expanded soon at the 'reshape()' below!
            self.lv2 = 0 # Same here. The method is a little bit dumb.
            # Fixme: Allow users to choose default language from preference
            # Temporally set English by default
            self.defaultLang = 'en'
            # This maps from line key of an entry to language code and Voice ID for its text
            # TODO: When completely merged ATTS, langMap will be replaced by ttsMap
            self.langMap = {'atop': [self.defaultLang, None]}
            self.ttsMap = {'atop': None}

            self.reshape(lv1=1, lv2=1)


        def reshape(self, lv1=None, lv2=None):
            if lv1 and (self.lv1 != lv1):
                self.lv1 = lv1
                self._reshape()
            if lv2 and (self.lv2 != lv2):
                self.lv2 = lv2
                self._reshape()

            print("EntrySetting: LangMap -> ", self.langMap)
            print("EntrySetting: ttsMap -> ", self.ttsMap)

        def _reshape(self):
            # Expand langMap and tags with default value
            for i in range(0, self.lv1):
                if 'def-%d' % (i + 1) not in self.ttsMap:
                    self.ttsMap['def-%d' % (i + 1)] = None
                # TODO: Replace langMap with ttsMap at all
                try:
                    self.langMap['def-%d' % (i + 1)]
                except KeyError:
                    self.langMap['def-%d' % (i + 1)] = [self.defaultLang, None]
                for j in range(0, self.lv2):
                    if 'ex-%d-%d' % (i + 1, j + 1) not in self.ttsMap:
                        self.ttsMap['ex-%d-%d' % (i + 1, j + 1)] = None
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
            data = {'lv1': self.lv1,
                    'lv2': self.lv2,
                    'langMap': None}
            langMap = {'atop': self.langMap['atop']}

            for i in range(0, self.lv1):
                langMap['def-%d' % (i + 1)] = self.langMap['def-%d' % (i + 1)]
                for j in range(0, self.lv2):
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
        from gui.widgets.entry import EntryWidget
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
