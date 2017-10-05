from gui.qt import *

class BundleUi(QListWidgetItem):
    def __init__(self):
        QListWidgetItem.__init__(self)

class BundleItemUi(QWidget):
    def __init__(self, fm, bundle, parent=None):
        super(BundleItemUi, self).__init__(parent)
        self.initFont()
        self.bundle = bundle
        self.fm = fm
        self.pref = fm.pref
        self.defEdits = []
        self.exEdits = []
        self.setupUi()

    # Fixme: The UI setup is too messy!
    def setupUi(self):
        # Definitions per bundle and Examples per definition
        dpb, epd = self.pref['dpb'], self.pref['epd']
        namelabel = QLabel("%d. %s" % (self.bundle.index, self.bundle.name))
        namelabel.setFont(self.boldFont)

        grid = QGridLayout()
        row = 1
        for i in range(1, dpb+1):
            dlbl = QLabel("Def%d" % i)
            dlbl.setFont(self.italFont)
            dedt = QLineEdit()
            grid.addWidget(dlbl, row, 0)
            grid.addWidget(dedt, row, 1)
            self.defEdits.append(dedt)
            for j in range(1, epd+1):
                elbl = QLabel("Ex%d-%d" % (i, j))
                elbl.setFont(self.italFont)
                eedt = QLineEdit()
                grid.addWidget(elbl, row+1, 0)
                grid.addWidget(eedt, row+1, 1)
                self.exEdits.append(eedt)
                row += 1
            row += 1

        vbox = QVBoxLayout()
        vbox.addWidget(namelabel)
        vbox.addLayout(grid)

        self.setLayout(vbox)

    def initFont(self):
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.italFont = QFont()
        self.italFont.setItalic(True)

    def toUpdate(self):
        return self.bundle.toUpdateUi

    def setBundleUpdateState(self, state):
        self.fm.setBundleUpdateState(self.bundle, state)

    def updateEditors(self):
        # Fixme: Need to operate labels and editors better way than with simple lists
        # Definitions per bundle and Examples per definition
        dpb, epd = self.fm.pref['dpb'], self.fm.pref['epd']

        for i, dedt in enumerate(self.defEdits[0:min(len(self.defEdits), dpb)]):
            try:
                dedt.setText(self.bundle.items[i]['define'])
                dedt.setCursorPosition(0)
            except (KeyError, IndexError):
                print("Cannot find definition %d of %s" % (i+1, self.bundle.name))
                continue

            for j, eedt in enumerate(self.exEdits[i*epd:(i+1)*epd]):
                try:
                    eedt.setText(self.bundle.items[i]['example'])
                    eedt.setCursorPosition(0)
                except (KeyError, IndexError):
                    print("Cannot find ex%d-%d of %s" % (i+1, j+1, self.bundle.name))
                    continue
