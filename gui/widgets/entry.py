from gui.qt import *

class Indexer(QSpinBox):
    def __init__(self, val):
        super(Indexer, self).__init__()
        self.setObjectName("index")
        self.setValue(val)
        self.setFixedWidth(40)
        self.setFocusPolicy(Qt.StrongFocus)

    def stepBy(self, stepBy):
        super().stepBy(-stepBy)


class EntryWidget(QWidget):
    # Design of QLabel shown on 'View' mode
    _ENTRY_VIEW = '<html><head/><body>{content}</body></html>'
    _FONT_TOP = '<p><span style=" font-size:16pt; font-weight:600;">{atop}</span></p>'
    _FONT_DEF = '<p>{num}. {define}</p>'
    _FONT_EX = '<p><span style="color:#8d8d8d;">&quot;{ex}&quot;</span></p>'

    move = pyqtSignal(int, int)
    delete = pyqtSignal(int)

    def __init__(self, parent, row, atop, mode, eset):
        super(EntryWidget, self).__init__(parent)
        self.initFont()
        # the EntryList this entry belongs to
        self.parent = parent
        # Row at EntryList takes from 0 to list.count()-1
        self.row = row
        self.mode = mode
        # Entry setting
        self.lv1 = eset['lv1']
        self.lv2 = eset['lv2']
        # External sources where the items of an entry came
        self.sources = []

        # Dictionary of QLineEdit.
        # The keys, referenced as 'lineKey', come in 'atop', 'def-n', 'ex-n-n' where 0 < n < 10
        # The name of keys must not be modified because we alphabetically sort them out in a process
        # Text stored in the editors will be the actual contents of printed or audio output
        self.editors = {}

        self.layout = QStackedLayout()
        self.setupUi(atop)

    def _control(self):
        """
        :return: QVBoxLayout
        ========
        Returns the left side of the layout of EntryWidget on View Mode,
        which contains delete button and spin box to move up and down the widget.
        """
        delete = QPushButton("X")
        delete.setFixedWidth(30)
        delete.clicked.connect(lambda: self.delete.emit(self.row))
        index = Indexer(self.row + 1)
        index.valueChanged.connect(self._move_to)

        layout = QVBoxLayout()
        layout.addWidget(delete, 0, Qt.AlignTop)
        layout.addWidget(index)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        return layout

    def _move_to(self, next):
        next -= 1 # Converts index to row of list.count()
        if next == self.row:
            # When spin.setValue triggers this method
            return

        if not 0 <= next < self.parent.count():
            spin = self.findChild(QSpinBox, "index")
            spin.setValue(self.row + 1)
        else:
            self.move.emit(self.row, next)

    def update_index(self, row):
        index = self.findChild(QSpinBox, "index")
        index.valueChanged.disconnect()
        index.setValue(row + 1)
        index.valueChanged.connect(self._move_to)
        self.row = row

    def setupUi(self, atop):
        self.setupView(atop)
        self.setupEditors(atop)
        self.setLayout(self.layout)
        if self.mode == "View":
            self.layout.setCurrentIndex(0)
        if self.mode == "Edit":
            self.layout.setCurrentIndex(1)

    def stringIndex(self):
        # Return string number from 00000 to 99999 based on the index
        index = self.row + 1
        snum = (5 - len(str(index))) * '0' + str(index)
        return snum

    def setMode(self, newMode):
        if newMode == self.mode: return

        if newMode == "View":
            self.layout.setCurrentIndex(0)
            self.mode = newMode
        if newMode == "Edit":
            self.layout.setCurrentIndex(1)
            self.mode = newMode

    def setupView(self, atop):
        viewWidget = QWidget()
        viewLayout = QHBoxLayout()
        viewLayout.addLayout(self._control())
        self.viewLabel = QLabel()
        self.viewLabel.setWordWrap(True)

        if atop == '':
            atop = "Empty entry"

        self.viewLabel.setText(self._ENTRY_VIEW.format
                           (content=self._FONT_TOP.format(atop=atop)))
        viewLayout.addWidget(self.viewLabel)
        viewWidget.setLayout(viewLayout)
        self.layout.addWidget(viewWidget)

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

        self.layout.addWidget(editWidget)

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
        content = self._FONT_TOP.format(num=self.row+1, atop=atop)

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

