from gui.qt import *

class FrameList(QListWidget):

    class Setting:
        def __init__(self):
            # Fixme: ...................
            self.dpw = 0 # Will be expanded soon later at the 'expand()' below!
            self.epd = 0 # Same here. The method is a bit dumb though.
            # Fixme: Allow users to choose default language from preference
            # Temporally set English by default
            self.defaultLang = 'en'
            self.langMap = {'name': self.defaultLang}

            self.expand(dpw=1, epd=1)


        def expand(self, dpw=None, epd=None):
            if dpw and (self.dpw < dpw):
                self.dpw = dpw
                self.expandLangMap()
            if epd and (self.epd < epd):
                self.epd = epd
                self.expandLangMap()

            print("FrameSetting: LangMap -> ", self.langMap)

        def expandLangMap(self):
            for i in range(0, self.dpw):
                try:
                    self.langMap['def-%d' % (i + 1)]
                except KeyError:
                    self.langMap['def-%d' % (i + 1)] = self.defaultLang
                for j in range(0, self.epd):
                    try:
                        self.langMap['ex-%d-%d' % (i + 1, j + 1)]
                    except KeyError:
                        self.langMap['ex-%d-%d' % (i + 1, j + 1)] = self.defaultLang

        # Returns the class' properties in a dictionary. Will be called on saving.
        def data(self):
            data = {'dpw': self.dpw,
                    'epd': self.epd,
                    'langMap': None}
            langMap = {'name': self.langMap['name']}

            for i in range(0, self.dpw):
                langMap['def-%d' % (i + 1)] = self.langMap['def-%d' % (i + 1)]
                for j in range(0, self.epd):
                    langMap['ex-%d-%d' % (i + 1, j + 1)] = self.langMap['ex-%d-%d' % (i + 1, j + 1)]

            data['langMap'] = langMap
            return data

    def __init__(self, parent=None):
        super(FrameList, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)
        self.setting = self.Setting()

    def createUi(self, index, name, mode, setting, parent=None):
        from gui.bundle import BundleWidget
        bui, bw = QListWidgetItem(), BundleWidget(index, name, mode, setting, parent=parent)
        bui.setSizeHint(bw.sizeHint())
        return bui, bw

    def updateBundle(self, name, items):
        for bw in self.getCurrentBundleWidgets():
            if bw.name == name:
                bw.updateEditors(items)
                return
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)

    def addBundle(self, name, mode, setting=None):
        if not setting:
            setting = self.setting.data()
        if name == '': pass
        elif name in [bw.name for bw in self.getCurrentBundleWidgets()]:
            print("Bundle with name %s already exists." % name)
            return

        bui, bw = self.createUi(self.count() + 1, name, mode, setting, parent=self)

        self.setting.expand(dpw=bw.dpw, epd=bw.epd)

        self.addItem(bui)
        self.setItemWidget(bui, bw)

    def deleteBundle(self):
        for bui in self.selectedItems():
            bw = self.itemWidget(bui)
            self.takeItem(bw.index - 1)
            self.updateIndex()
        self._update()

    def deleteAll(self):
        for _ in range(self.count()):
            self.takeItem(0)

    def updateIndex(self):
        # Update index of bundles after Nth bundle
        for i in range(self.count()):
            bw = self.getBundleWidget(i)
            bw.index = i + 1

    # Fixme: Remove the leading underscore by rename it to 'updateAll'
    def _update(self):
        # Update the inside of the bundles in the list
        print("Bundle updates")
        for i in range(self.count()):
            bui = self.item(i)
            bw = self.itemWidget(bui)
            bw.index = i + 1
            bw.updateDisplay()
            bui.setSizeHint(bw.sizeHint())

        self.repaint()

    def updateMode(self, newMode):
        for bw in self.getCurrentBundleWidgets():
            bw.updateMode(newMode)

    def copyContents(self):
        for bw in self.getCurrentBundleWidgets():
            bw.editors['def-1'].setText(bw.editors['name'].text())

    def getBundle(self, name):
        for bw in self.getCurrentBundleWidgets():
            if bw.name == name:
                return bw
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)

    def getCurrentBundleWidgets(self):
        return [self.getBundleWidget(i) for i in range(self.count())]

    def getBundleWidget(self, index):
        return self.itemWidget(self.item(index))
