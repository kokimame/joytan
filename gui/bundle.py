from gui.qt import *

class BundleFactory:
    def __init__(self):
        # TODO: More should be coming
        self.pref = {
            "dpw": 2,
            "epd": 1
        }

    def createUi(self, index, bundle):
        bui, bitem = BundleUi(), BundleItemUi(index, bundle, self.pref)
        bui.setSizeHint(bitem.sizeHint())
        return bui, bitem


class BundleUi(QListWidgetItem):
    def __init__(self):
        QListWidgetItem.__init__(self)

class BundleItemUi(QWidget):
    def __init__(self, index, bundle, pref, parent=None):
        super(BundleItemUi, self).__init__(parent)
        self.initFont()
        self.index = index
        self.bundle = bundle
        self.name = bundle.name
        self.dpw = pref['dpw']
        self.epd = pref['epd']

        self.html = '<html><head/><body>{content}</body></html>'
        self.nameFormat = '<p><span style=" font-size:16pt; font-weight:600;">{num}. {name}</span></p>'
        self.defFormat = '<p>{num}. {define}</p>'
        self.exFormat = '<p><span style="color:#8d8d8d;">&quot;{example}&quot;</span></p>'
        self.editors = {}
        self.stackedLayout = QStackedLayout()
        self.mode = "Disp"

        self.setupUi()

    def setupUi(self):
        self.setupDisplay()
        self.setupEditors()
        self.setLayout(self.stackedLayout)

    def updateMode(self, newMode):
        if newMode == self.mode: return

        if newMode == "Disp":
            self.setEditingResult()
            self.stackedLayout.setCurrentIndex(0)
            self.mode = newMode
        if newMode == "Edit":
            self.stackedLayout.setCurrentIndex(1)
            self.mode = newMode

    def setupDisplay(self):
        dispWidget = QWidget()
        dispLayout = QVBoxLayout()
        editBtn = QPushButton("Edit")
        editBtn.clicked.connect(lambda: self.updateMode("Edit"))
        delBtn = QPushButton("Delete")
        btnBox = QHBoxLayout()
        btnBox.addWidget(editBtn)
        btnBox.addWidget(delBtn)
        btnBox.addStretch()
        dispLayout.addLayout(btnBox)

        self.label = QLabel()
        self.label.setText(self.html.format
                           (content=self.nameFormat.format(num=self.index, name=self.name)))
        dispLayout.addWidget(self.label)
        dispWidget.setLayout(dispLayout)
        self.stackedLayout.addWidget(dispWidget)

    def setupEditors(self):
        # Definitions per bundle and Examples per definition
        editWidget = QWidget()
        editLayout = QVBoxLayout()

        btnBox = QHBoxLayout()
        okBtn = QPushButton("OK")
        okBtn.clicked.connect(lambda: self.updateMode("Disp"))
        delBtn = QPushButton("Delete")
        btnBox.addWidget(okBtn)
        btnBox.addWidget(delBtn)
        btnBox.addStretch()
        editLayout.addLayout(btnBox)

        dpw, epd = self.dpw, self.epd
        namelabel = QLabel("%d. %s" % (self.index, self.name))
        namelabel.setFont(self.boldFont)
        editLayout.addWidget(namelabel)

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

        editLayout.addLayout(grid)
        editWidget.setLayout(editLayout)

        self.stackedLayout.addWidget(editWidget)


    def initFont(self):
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.italFont = QFont()
        self.italFont.setItalic(True)

    def update(self):
        self.updateDisplay()
        self.updateEditors()

    def updateDisplay(self):
        content = self.nameFormat.format(num=self.index, name=self.name)
        for i, item in enumerate(self.bundle.items):
            if i + 1 > self.dpw: break
            content += self.defFormat.format(num=(i+1), define=item['define'])
            for j, ex in enumerate(item['examples']):
                if j + 1 > self.epd: break
                if ex == '': continue
                content += self.exFormat.format(example=ex)

        self.label.setText(self.html.format(content=content))

    def setEditingResult(self):
        content = self.nameFormat.format(num=self.index, name=self.name)

        for i in range(1, self.dpw+1):
            define = self.editors['def-%d' % i].text()
            if define != '':
                content += self.defFormat.format(num=i, define=define)
            for j in range(1, self.epd+1):
                examp = self.editors['ex-%d-%d' % (i, j)].text()
                if examp != '':
                    content += self.exFormat.format(example=examp)
        self.label.setText(self.html.format(content=content))


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


