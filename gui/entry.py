from gui.qt import *


class EntryWidget(QWidget):
    def __init__(self, index, name, mode, pref, parent=None):
        super(EntryWidget, self).__init__(parent)
        self.initFont()
        self.parent = parent
        self.index = index
        self.name = name
        self.mode = mode
        self.dpw = pref['dpw']
        self.epd = pref['epd']
        # External sources where the items of an entry came
        self.sources = []

        self.html = '<html><head/><body>{content}</body></html>'
        self.nameFormat = '<p><span style=" font-size:16pt; font-weight:600;">{num}. {name}</span></p>'
        self.defFormat = '<p>{num}. {define}</p>'
        self.exFormat = '<p><span style="color:#8d8d8d;">&quot;{example}&quot;</span></p>'
        self.editors = {}
        self.stackedLayout = QStackedLayout()

        self.setupUi(name)

    def setupUi(self, name):
        self.setupView()
        self.setupEditors(name)
        self.setLayout(self.stackedLayout)
        if self.mode == "View":
            self.stackedLayout.setCurrentIndex(0)
        if self.mode == "Edit":
            self.stackedLayout.setCurrentIndex(1)

    def getDirname(self):
        # Make string number from the index of the entry from 00000 to 99999
        snum = (5 - len(str(self.index))) * '0' + str(self.index)
        # Return directory name replacing whitespace with underscore
        return "{snum}".format(snum=snum)

    def setMode(self, newMode):
        if newMode == self.mode: return

        if newMode == "View":
            self.stackedLayout.setCurrentIndex(0)
            self.mode = newMode
        if newMode == "Edit":
            self.stackedLayout.setCurrentIndex(1)
            self.mode = newMode

    def setupView(self):
        viewWidget = QWidget()
        viewLayout = QVBoxLayout()

        self.viewLabel = QLabel()

        if self.name == '':
            name = "Empty entry"
        else:
            name = self.name
        self.viewLabel.setText(self.html.format
                           (content=self.nameFormat.format(num=self.index, name=name)))
        viewLayout.addWidget(self.viewLabel)
        viewWidget.setLayout(viewLayout)
        self.stackedLayout.addWidget(viewWidget)

    def setupEditors(self, name):
        # Definitions per entry and Examples per definition
        editWidget = QWidget()
        editLayout = QGridLayout()

        namelabel = QLabel("Name")
        namelabel.setFont(self.italFont)
        namelabel.setStyleSheet("QLabel { background-color : rgb(255, 255, 180); }")
        nameedit = QLineEdit(name)
        editLayout.addWidget(namelabel, 0, 0)
        editLayout.addWidget(nameedit, 0, 1)
        self.editors["atop"] = nameedit

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

    def updateView(self):
        self.name = self.editors['atop'].text()
        if self.name == '':
            name = "Empty entry"
        else:
            name = self.name
        content = self.nameFormat.format(num=self.index, name=name)

        for i in range(0, self.dpw):
            if self.editors['def-%d' % (i+1)].text() != '':
                content += self.defFormat.format(num=i+1, define=self.editors['def-%d' % (i+1)].text())
            for j in range(0, self.epd):
                if self.editors['ex-%d-%d' % (i+1, j+1)].text() != '':
                    content += self.exFormat.format(example=self.editors['ex-%d-%d' % (i+1, j+1)].text())

        self.viewLabel.setText(self.html.format(content=content))

    # Set the text of downloaded contents to each of matched editors
    def updateEditors(self, items):
        for i in range(0, min(self.dpw, len(items))):
            self.editors['def-%d' % (i+1)].setText(items[i]['define'])
            for j in range(0, min(self.epd, len(items[i]['examples']))):
                self.editors['ex-%d-%d' % (i+1, j+1)].setText(items[i]['examples'][j])

    # Returns the class' properties in a dictionary. Will be called on saving.
    def data(self):
        data = {}
        data['atop'] = self.editors['atop'].text()
        data['dpw'] = self.dpw
        data['epd'] = self.epd
        for i in range(0, self.dpw):
            data['def-%d' % (i+1)] = self.editors['def-%d' % (i+1)].text()
            for j in range(self.epd):
                data['ex-%d-%d' % (i+1, j+1)] = self.editors['ex-%d-%d' % (i+1, j+1)].text()

        return data

