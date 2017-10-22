from gui.qt import *


class BundleFactory:
    class Bundle():
        # Bundle for a word containing a number of meaning and example usage of its word
        def __init__(self, name, index):
            self.name = name
            self.sources = []
            self.items = []

        def updateItems(self, items):
            self.items.extend(items)

    def __init__(self):
        # TODO: More should be coming
        self.pref = {
            "dpw": 1,       # Definitions per Bundle
            "epd": 1        # Examples per Definition
        }

    def makeBundle(self, name, index):
        return BundleFactory.Bundle(name, index)

    def createUi(self, index, bundle, mode, parent=None):
        bui, bw = BundleUi(), BundleWidget(index, bundle, mode, self.pref, parent=parent)
        bui.setSizeHint(bw.sizeHint())
        return bui, bw

class BundleUi(QListWidgetItem):
    def __init__(self):
        QListWidgetItem.__init__(self)

class BundleWidget(QWidget):
    def __init__(self, index, bundle, mode, pref, parent=None):
        super(BundleWidget, self).__init__(parent)
        self.initFont()
        self.parent = parent
        self.index = index
        self.bundle = bundle
        self.mode = mode
        self.dpw = pref['dpw']
        self.epd = pref['epd']

        self.html = '<html><head/><body>{content}</body></html>'
        self.nameFormat = '<p><span style=" font-size:16pt; font-weight:600;">{num}. {name}</span></p>'
        self.defFormat = '<p>{num}. {define}</p>'
        self.exFormat = '<p><span style="color:#8d8d8d;">&quot;{example}&quot;</span></p>'
        self.editors = {}
        self.stackedLayout = QStackedLayout()

        self.setupUi(bundle.name)

    def setupUi(self, name):
        self.setupDisplay()
        self.setupEditors(name)
        self.setLayout(self.stackedLayout)
        if self.mode == "Disp":
            self.stackedLayout.setCurrentIndex(0)
        if self.mode == "Edit":
            self.stackedLayout.setCurrentIndex(1)

    def getDirname(self):
        # Make string number from the index of the bundle from 00000 to 99999
        snum = (5 - len(str(self.index))) * '0' + str(self.index)
        # Return directory name replacing whitespace with underscore
        return "{snum}-{name}".format(snum=snum, name=self.bundle.name.replace(" ", "_"))

    def updateMode(self, newMode):
        if newMode == self.mode: return

        if newMode == "Disp":
            # Save editing result before changing to Display mode
            self.saveEditors()
            self.stackedLayout.setCurrentIndex(0)
            self.mode = newMode
        if newMode == "Edit":
            self.stackedLayout.setCurrentIndex(1)
            self.mode = newMode

    def deleteSelf(self):
        self.parent.deleteUi(self)

    def setupDisplay(self):
        dispWidget = QWidget()
        dispLayout = QVBoxLayout()

        self.dispLabel = QLabel()

        if self.bundle.name == '':
            name = "Anonymous bundle"
        else:
            name = self.bundle.name
        self.dispLabel.setText(self.html.format
                           (content=self.nameFormat.format(num=self.index, name=name)))
        dispLayout.addWidget(self.dispLabel)
        dispWidget.setLayout(dispLayout)
        self.stackedLayout.addWidget(dispWidget)

    def setupEditors(self, name):
        # Definitions per bundle and Examples per definition
        editWidget = QWidget()
        editLayout = QGridLayout()

        namelabel = QLabel("Name")
        namelabel.setFont(self.italFont)
        namelabel.setStyleSheet("QLabel { background-color : rgb(255, 255, 180); }")
        nameedit = QLineEdit(name)
        editLayout.addWidget(namelabel, 0, 0)
        editLayout.addWidget(nameedit, 0, 1)
        self.editors["name"] = nameedit

        row = 1
        dpw, epd = self.dpw, self.epd
        for i in range(1, dpw+1):
            deflabel = QLabel("Def%d" % i)
            deflabel.setFont(self.italFont)
            deflabel.setStyleSheet("QLabel { background-color : rgb(255, 180, 230); }")
            defedit = QLineEdit()
            editLayout.addWidget(deflabel, row, 0)
            editLayout.addWidget(defedit, row, 1)
            self.editors["def-%d" % i] = defedit
            for j in range(1, epd+1):
                exlabel = QLabel("Ex%d-%d" % (i, j))
                exlabel.setFont(self.italFont)
                exlabel.setStyleSheet("QLabel { background-color : rgb(180, 230, 255); }")
                exedit = QLineEdit()
                editLayout.addWidget(exlabel, row+1, 0)
                editLayout.addWidget(exedit, row+1, 1)
                self.editors["ex-%d-%d" % (i, j)] = exedit
                row += 1
            row += 1

        editWidget.setLayout(editLayout)

        self.stackedLayout.addWidget(editWidget)


    def initFont(self):
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.italFont = QFont()
        self.italFont.setItalic(True)

    def updateUi(self):
        self.updateDisplay()
        self.updateEditors()

    def updateDisplay(self):
        if self.bundle.name == '':
            name = "Anonymous bundle"
        else:
            name = self.bundle.name
        content = self.nameFormat.format(num=self.index, name=name)
        for i, item in enumerate(self.bundle.items):
            if i + 1 > self.dpw: break
            content += self.defFormat.format(num=(i+1), define=item['define'])
            for j, ex in enumerate(item['examples']):
                if j + 1 > self.epd: break
                if ex == '': continue
                content += self.exFormat.format(example=ex)

        self.dispLabel.setText(self.html.format(content=content))

    def saveEditors(self):
        self.bundle.name = self.editors['name'].text()
        if self.bundle.name == '':
            name = "Anonymous bundle"
        else:
            name = self.bundle.name
        content = self.nameFormat.format(num=self.index, name=name)

        for i in range(1, self.dpw+1):
            define = self.editors['def-%d' % i].text()
            if define != '':
                content += self.defFormat.format(num=i, define=define)
            for j in range(1, self.epd+1):
                examp = self.editors['ex-%d-%d' % (i, j)].text()
                if examp != '':
                    content += self.exFormat.format(example=examp)
        self.dispLabel.setText(self.html.format(content=content))


    def updateEditors(self):
        for key, editor in self.editors.items():
            if key == "name":
                editor.setText(self.bundle.name)
                continue
            keys = list(key.split("-"))
            if keys[0] == "def":
                num = int(keys[1]) - 1
                try:
                    editor.setText(self.bundle.items[num]['define'])
                    editor.setCursorPosition(0)
                except (KeyError, IndexError):
                    print("Error : Editor cannot update", key)
            elif keys[0] == "ex":
                num1, num2 = int(keys[1]) - 1, int(keys[2]) - 1
                try:
                    editor.setText(self.bundle.items[num1]['examples'][num2])
                    editor.setCursorPosition(0)
                except (KeyError, IndexError):
                    print("Error : Editor cannot update", key)
            else:
                print("Error: Unknown editor type '%s' found" % key)
                sys.exit(1)


