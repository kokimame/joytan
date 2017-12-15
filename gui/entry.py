from gui.qt import *


class EntryWidget(QWidget):
    def __init__(self, index, atop, mode, eset, parent=None):
        super(EntryWidget, self).__init__(parent)
        self.initFont()
        self.parent = parent
        self.index = index
        self.mode = mode
        # Entry setting
        self.lv1 = eset['lv1']
        self.lv2 = eset['lv2']
        # External sources where the items of an entry came
        self.sources = []

        # QLineEdit dictionary.
        # The keys, referenced as 'lineKey', come in 'atop', 'def-n', 'ex-n-n' where 0 < n < 10
        # The name of keys must not be modified because we alphabetically sort them out in a process
        # Text stored in the editors will be the actual contents of printed or audio output
        self.editors = {}

        # Design of QLabel shown on 'View' mode
        self.html = '<html><head/><body>{content}</body></html>'
        self.atopFormat = '<p><span style=" font-size:16pt; font-weight:600;">{num}. {atop}</span></p>'
        self.defFormat = '<p>{num}. {define}</p>'
        self.exFormat = '<p><span style="color:#8d8d8d;">&quot;{example}&quot;</span></p>'

        self.stackedLayout = QStackedLayout()
        self.setupUi(atop)

    def setupUi(self, atop):
        self.setupView(atop)
        self.setupEditors(atop)
        self.setLayout(self.stackedLayout)
        if self.mode == "View":
            self.stackedLayout.setCurrentIndex(0)
        if self.mode == "Edit":
            self.stackedLayout.setCurrentIndex(1)

    def getDirname(self):
        # Make string number from the index of the entry from 00000 to 99999
        snum = (5 - len(str(self.index))) * '0' + str(self.index)
        # Return directory atop replacing whitespace with underscore
        return "{snum}".format(snum=snum)

    def setMode(self, newMode):
        if newMode == self.mode: return

        if newMode == "View":
            self.stackedLayout.setCurrentIndex(0)
            self.mode = newMode
        if newMode == "Edit":
            self.stackedLayout.setCurrentIndex(1)
            self.mode = newMode

    def setupView(self, atop):
        viewWidget = QWidget()
        viewLayout = QVBoxLayout()

        self.viewLabel = QLabel()

        if atop == '':
            atop = "Empty entry"

        self.viewLabel.setText(self.html.format
                           (content=self.atopFormat.format(num=self.index, atop=atop)))
        viewLayout.addWidget(self.viewLabel)
        viewWidget.setLayout(viewLayout)
        self.stackedLayout.addWidget(viewWidget)

    def setupEditors(self, atop):
        # Definitions per entry and Examples per definition
        editWidget = QWidget()
        editLayout = QGridLayout()

        atopLabel = QLabel('atop')
        atopLabel.setFont(self.italFont)
        atopLabel.setStyleSheet("QLabel { background-color : rgb(255, 255, 180); }")
        atopEdit = QLineEdit(atop)
        editLayout.addWidget(atopLabel, 0, 0)
        editLayout.addWidget(atopEdit, 0, 1)
        self.editors["atop"] = atopEdit

        row = 1
        for i in range(0, self.lv1):
            defLabel = QLabel('def-%d' % (i+1))
            defLabel.setFont(self.italFont)
            defLabel.setStyleSheet("QLabel { background-color : rgb(255, 180, 230); }")
            defEdit = QLineEdit()
            editLayout.addWidget(defLabel, row, 0)
            editLayout.addWidget(defEdit, row, 1)
            self.editors["def-%d" % (i+1)] = defEdit
            for j in range(0, self.lv2):
                exLabel = QLabel('ex-%d-%d' % (i+1, j+1))
                exLabel.setFont(self.italFont)
                exLabel.setStyleSheet("QLabel { background-color : rgb(180, 230, 255); }")
                exEdit = QLineEdit()
                editLayout.addWidget(exLabel, row+1, 0)
                editLayout.addWidget(exEdit, row+1, 1)
                self.editors["ex-%d-%d" % (i+1, j+1)] = exEdit
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
        self.atop = self.editors['atop'].text()
        if self.atop == '':
            atop = "Empty entry"
        else:
            atop = self.atop
        content = self.atopFormat.format(num=self.index, atop=atop)

        for i in range(0, self.lv1):
            if self.editors['def-%d' % (i+1)].text() != '':
                content += self.defFormat.format(num=i+1, define=self.editors['def-%d' % (i+1)].text())
            for j in range(0, self.lv2):
                if self.editors['ex-%d-%d' % (i+1, j+1)].text() != '':
                    content += self.exFormat.format(example=self.editors['ex-%d-%d' % (i+1, j+1)].text())

        self.viewLabel.setText(self.html.format(content=content))

    # Set the text of downloaded contents to each of matched editors
    def updateEditors(self, items):
        for i in range(0, min(self.lv1, len(items))):
            self.editors['def-%d' % (i+1)].setText(items[i]['define'])
            for j in range(0, min(self.lv2, len(items[i]['examples']))):
                self.editors['ex-%d-%d' % (i+1, j+1)].setText(items[i]['examples'][j])

    # Returns the class' properties in a dictionary. Will be called on saving.
    def data(self):
        data = {}
        data['atop'] = self.editors['atop'].text()
        data['lv1'] = self.lv1
        data['lv2'] = self.lv2
        for i in range(0, self.lv1):
            data['def-%d' % (i+1)] = self.editors['def-%d' % (i+1)].text()
            for j in range(self.lv2):
                data['ex-%d-%d' % (i+1, j+1)] = self.editors['ex-%d-%d' % (i+1, j+1)].text()

        return data

