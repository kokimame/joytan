from gui.qt import *


class BundleFactory:
    def __init__(self):
        # TODO: More should be coming
        self.pref = {
            "dpw": 1,       # Definitions per Bundle
            "epd": 1        # Examples per Definition
        }

    def createUi(self, index, name, mode, parent=None):
        bui, bw = QListWidgetItem(), BundleWidget(index, name, mode, self.pref, parent=parent)
        bui.setSizeHint(bw.sizeHint())
        return bui, bw


class BundleWidget(QWidget):
    def __init__(self, index, name, mode, pref, parent=None):
        super(BundleWidget, self).__init__(parent)
        self.initFont()
        self.parent = parent
        self.index = index
        self.name = name
        self.mode = mode
        self.dpw = pref['dpw']
        self.epd = pref['epd']
        # External sources that the bundle used
        self.sources = []

        self.html = '<html><head/><body>{content}</body></html>'
        self.nameFormat = '<p><span style=" font-size:16pt; font-weight:600;">{num}. {name}</span></p>'
        self.defFormat = '<p>{num}. {define}</p>'
        self.exFormat = '<p><span style="color:#8d8d8d;">&quot;{example}&quot;</span></p>'
        self.editors = {}
        self.stackedLayout = QStackedLayout()

        self.setupUi(name)

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
        return "{snum}".format(snum=snum)

    def updateMode(self, newMode):
        if newMode == self.mode: return

        if newMode == "Disp":
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

        if self.name == '':
            name = "Anonymous bundle"
        else:
            name = self.name
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
        for i in range(0, self.dpw):
            deflabel = QLabel("Def%d" % (i+1))
            deflabel.setFont(self.italFont)
            deflabel.setStyleSheet("QLabel { background-color : rgb(255, 180, 230); }")
            defedit = QLineEdit()
            editLayout.addWidget(deflabel, row, 0)
            editLayout.addWidget(defedit, row, 1)
            self.editors["def-%d" % (i+1)] = defedit
            for j in range(0, self.epd):
                exlabel = QLabel("Ex%d-%d" % (i+1, j+1))
                exlabel.setFont(self.italFont)
                exlabel.setStyleSheet("QLabel { background-color : rgb(180, 230, 255); }")
                exedit = QLineEdit()
                editLayout.addWidget(exlabel, row+1, 0)
                editLayout.addWidget(exedit, row+1, 1)
                self.editors["ex-%d-%d" % (i+1, j+1)] = exedit
                row += 1
            row += 1

        editWidget.setLayout(editLayout)

        self.stackedLayout.addWidget(editWidget)

    def initFont(self):
        self.boldFont = QFont()
        self.boldFont.setBold(True)
        self.italFont = QFont()
        self.italFont.setItalic(True)

    def updateDisplay(self):
        self.name = self.editors['name'].text()
        if self.name == '':
            name = "Anonymous bundle"
        else:
            name = self.name
        content = self.nameFormat.format(num=self.index, name=name)

        for i in range(0, self.dpw):
            if self.editors['def-%d' % (i+1)].text() != '':
                content += self.defFormat.format(num=i+1, define=self.editors['def-%d' % (i+1)].text())
            for j in range(0, self.epd):
                if self.editors['ex-%d-%d' % (i+1, j+1)].text() != '':
                    content += self.exFormat.format(example=self.editors['ex-%d-%d' % (i+1, j+1)].text())

        self.dispLabel.setText(self.html.format(content=content))

    # Set the text of downloaded contents to each of matched editors
    def updateEditors(self, items):
        for i in range(0, min(self.dpw, len(items))):
            self.editors['def-%d' % (i+1)].setText(items[i]['define'])
            for j in range(0, min(self.epd, len(items[i]['examples']))):
                self.editors['ex-%d-%d' % (i+1, j+1)].setText(items[i]['examples'][j])

