from gui.qt import *

class BundleFactory:
    def __init__(self):
        # TODO: More should be coming
        self.pref = {
            "dpw": 2,
            "epd": 1
        }

    def createUi(self, bundle):
        bui, bitem = BundleUi(), BundleItemUi(bundle, self.pref)
        bui.setSizeHint(bitem.sizeHint())
        return bui, bitem


class BundleUi(QListWidgetItem):
    def __init__(self):
        QListWidgetItem.__init__(self)

class BundleItemUi(QWidget):
    def __init__(self, bundle, pref, parent=None):
        super(BundleItemUi, self).__init__(parent)
        self.initFont()
        self.bundle = bundle
        self.name = bundle.name
        self.dpw = pref['dpw']
        self.epd = pref['epd']

        self.editors = {}
        self.setupUi()

    def setupUi(self):
        # Definitions per bundle and Examples per definition
        dpw, epd = self.dpw, self.epd
        namelabel = QLabel("%d. %s" % (self.bundle.index, self.name))
        namelabel.setFont(self.boldFont)

        grid = QGridLayout()
        row = 1
        for i in range(1, dpw+1):
            deflabel = QLabel("Def%d" % i)
            deflabel.setFont(self.italFont)
            deflabel.setStyleSheet("QLabel { background-color : rgb(255, 180, 230); }")
            defedit = QLineEdit()
            grid.addWidget(deflabel, row, 0)
            grid.addWidget(defedit, row, 1)
            self.editors["def-%d" % i] = defedit
            for j in range(1, epd+1):
                exlabel = QLabel("Ex%d-%d" % (i, j))
                exlabel.setFont(self.italFont)
                exlabel.setStyleSheet("QLabel { background-color : rgb(180, 230, 255); }")
                exedit = QLineEdit()
                grid.addWidget(exlabel, row+1, 0)
                grid.addWidget(exedit, row+1, 1)
                self.editors["ex-%d-%d" % (i, j)] = exedit
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

    def updateEditors(self):
        for key, editor in self.editors.items():
            keys = list(key.split("-"))
            if keys[0] == "def":
                num = int(keys[1]) - 1
                try:
                    editor.setText(self.bundle.items[num]['define'])
                    editor.setCursorPosition(0)
                except (KeyError, IndexError):
                    print("Error : Editor update", key)
            elif keys[0] == "ex":
                num1, num2 = int(keys[1]) - 1, int(keys[2]) - 1
                try:
                    print(self.bundle, self.bundle.items)
                    editor.setText(self.bundle.items[num1]['examples'][num2])
                    editor.setCursorPosition(0)
                except (KeyError, IndexError):
                    print("Error : Editor update", key)
            else:
                print("Error: Unknown editor type found")
                sys.exit(1)


