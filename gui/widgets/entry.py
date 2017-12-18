from gui.qt import *


class EntryWidget(QWidget):
    # Design of QLabel shown on 'View' mode
    _ENTRY_VIEW = '<html><head/><body>{content}</body></html>'
    _FONT_TOP = '<p><span style=" font-size:16pt; font-weight:600;">{num}. {atop}</span></p>'
    _FONT_DEF = '<p>{num}. {define}</p>'
    _FONT_EX = '<p><span style="color:#8d8d8d;">&quot;{ex}&quot;</span></p>'

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

    def stringIndex(self):
        # Return string number from 00000 to 99999 based on the index
        snum = (5 - len(str(self.index))) * '0' + str(self.index)
        return snum

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
        self.viewLabel.setWordWrap(True)

        if atop == '':
            atop = "Empty entry"

        self.viewLabel.setText(self._ENTRY_VIEW.format
                           (content=self._FONT_TOP.format(num=self.index, atop=atop)))
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
        for i in range(1, self.lv1 + 1):
            defLabel = QLabel('def-%d' % i)
            defLabel.setFont(self.italFont)
            defLabel.setStyleSheet("QLabel { background-color : rgb(255, 180, 230); }")
            defEdit = QLineEdit()
            editLayout.addWidget(defLabel, row, 0)
            editLayout.addWidget(defEdit, row, 1)
            self.editors["def-%d" % i] = defEdit
            for j in range(1, self.lv2 + 1):
                exLabel = QLabel('ex-%d-%d' % (i, j))
                exLabel.setFont(self.italFont)
                exLabel.setStyleSheet("QLabel { background-color : rgb(180, 230, 255); }")
                exEdit = QLineEdit()
                editLayout.addWidget(exLabel, row+1, 0)
                editLayout.addWidget(exEdit, row+1, 1)
                self.editors["ex-%d-%d" % (i, j)] = exEdit
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
        content = self._FONT_TOP.format(num=self.index, atop=atop)

        for i in range(1, self.lv1 + 1):
            if self.editors['def-%d' % i].text() != '':
                content += self._FONT_DEF.format(num=i, define=self.editors['def-%d' % i].text())
            for j in range(1, self.lv2 + 1):
                if self.editors['ex-%d-%d' % (i, j)].text() != '':
                    content += self._FONT_EX.format(ex=self.editors['ex-%d-%d' % (i, j)].text())

        self.viewLabel.setText(self._ENTRY_VIEW.format(content=content))

    # Set the text of downloaded contents to each of matched editors
    def updateEditors(self, items):
        if 'atop' in items:
            self.editors['atop'].setText(items['atop'])

        for i in range(1, self.lv1 + 1):
            if 'def-%d' % i in items:
                self.editors['def-%d' % i].setText(items['def-%d' % i])
            for j in range(1, self.lv2 + 1):
                if 'ex-%d-%d' % (i, j) in items:
                    self.editors['ex-%d-%d' % (i, j)].setText(items['ex-%d-%d' % (i, j)])

    # Returns the class' properties in a dictionary. Will be called on saving.
    def data(self):
        data = {}
        data['atop'] = self.editors['atop'].text()
        data['lv1'] = self.lv1
        data['lv2'] = self.lv2
        for i in range(1, self.lv1 + 1):
            data['def-%d' % i] = self.editors['def-%d' % i].text()
            for j in range(1, self.lv2 + 1):
                data['ex-%d-%d' % (i, j)] = self.editors['ex-%d-%d' % (i, j)].text()

        return data

