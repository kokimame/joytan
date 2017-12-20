from gui.qt import *


class Indexer(QSpinBox):
    def __init__(self, val):
        super(Indexer, self).__init__()
        self.setObjectName("index")
        self.setValue(val)
        self.setFixedWidth(40)
        self.setFocusPolicy(Qt.StrongFocus)

    def stepBy(self, step):
        # Change default down-button to increase the number and vice versa.
        super().stepBy(-step)


class EntryWidget(QWidget):
    # Design of QLabel shown on 'View' mode
    _ENTRY_VIEW = '<html><head/><body>{content}</body></html>'
    _FONT_TOP = '<p><span style=" font-size:16pt; font-weight:600;">{atop}</span></p>'
    _FONT_DEF = '<p>{num}. {define}</p>'
    _FONT_EX = '<p><span style="color:#8d8d8d;">&quot;{ex}&quot;</span></p>'

    _BOLD, _ITALIC = QFont(), QFont()
    _BOLD.setBold(True)
    _ITALIC.setItalic(True)

    move = pyqtSignal(int, int)
    delete = pyqtSignal(int)

    def __init__(self, parent, row, atop, mode, eset):
        super(EntryWidget, self).__init__(parent)
        # the EntryList this entry belongs to
        self.parent = parent
        # Row at EntryList takes from 0 to list.count()-1
        self.row = row
        self.atop = atop
        self.mode = mode
        # Entry setting
        self.lv1 = eset['lv1']
        self.lv2 = eset['lv2']
        # External sources where the items of an entry came
        self.sources = []

        # Dictionary of QLineEdit.
        # Text stored in the editors will be the actual learning materials.
        # The keys, referenced as '_key' (with underscode), come in 'atop', 'def-n', 'ex-n-n' where 0 < n < 10
        # ===
        # 'atop' : The name of Entry. Should be identical in the parent.
        # 'def-x' : Main part of an Entry. Each entry has upto 9 of this section.
        # 'ex-x-x' : Sub part. Each 'def-x' has upto 9 of the sub section.
        # ===
        # NOTE: The name of keys must not be modified because we alphabetically sort them out in a process
        self.editors = {}

        # Building UI
        layout = QStackedLayout()
        layout.setObjectName("layout")
        layout.addWidget(self._ui_view(atop))
        layout.addWidget(self._ui_editor(atop))
        self.set_mode(mode)
        self.setLayout(layout)

    def set_mode(self, new_mode):
        if new_mode == self.mode:
            return

        layout = self.findChild(QStackedLayout, "layout")
        if new_mode == "View":
            layout.setCurrentIndex(0)
            self.mode = new_mode
        if new_mode == "Edit":
            layout.setCurrentIndex(1)
            self.mode = new_mode

    def _control(self):
        """
        :return: QVBoxLayout
        ========
        Returns the left side of the layout of EntryWidget on View Mode,
        which contains delete button and spin box to move up and down the widget.
        """
        delete = QPushButton("x")
        delete.setFixedWidth(23)
        delete.setFixedHeight(23)
        delete.setStyleSheet("QPushButton { background-color: rgb(180,180,180); }")
        delete.clicked.connect(lambda: self.delete.emit(self.row))
        index = Indexer(self.row + 1)
        index.valueChanged.connect(self._move_to)

        layout = QVBoxLayout()
        layout.addWidget(delete, 0, Qt.AlignTop)
        layout.addWidget(index)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        return layout

    def _ui_view(self, atop):
        view = QLabel()
        view.setWordWrap(True)
        view.setObjectName("view")

        if atop == '':
            atop = "Empty entry"

        view.setText(self._ENTRY_VIEW.format
                     (content=self._FONT_TOP.format(atop=atop)))

        layout = QHBoxLayout()
        layout.addLayout(self._control())
        layout.addWidget(view)
        base = QWidget()
        base.setLayout(layout)
        return base

    def _ui_editor(self, atop):
        # Definitions per entry and Examples per definition
        a_lbl = QLabel('atop')
        a_lbl.setFont(self._ITALIC)
        a_lbl.setStyleSheet("QLabel { background-color : rgb(255, 255, 180); }")
        a_edit = QLineEdit(atop)
        self.editors["atop"] = a_edit

        layout = QGridLayout()
        layout.addWidget(a_lbl, 0, 0)
        layout.addWidget(a_edit, 0, 1)
        row = 1
        for i in range(1, self.lv1 + 1):
            d_lbl = QLabel('def-%d' % i)
            d_lbl.setFont(self._ITALIC)
            d_lbl.setStyleSheet("QLabel { background-color : rgb(255, 180, 230); }")
            d_edit = QLineEdit()
            layout.addWidget(d_lbl, row, 0)
            layout.addWidget(d_edit, row, 1)
            self.editors["def-%d" % i] = d_edit
            for j in range(1, self.lv2 + 1):
                e_lbl = QLabel('ex-%d-%d' % (i, j))
                e_lbl.setFont(self._ITALIC)
                e_lbl.setStyleSheet("QLabel { background-color : rgb(180, 230, 255); }")
                e_edit = QLineEdit()
                layout.addWidget(e_lbl, row+1, 0)
                layout.addWidget(e_edit, row+1, 1)
                self.editors["ex-%d-%d" % (i, j)] = e_edit
                row += 1
            row += 1

        base = QWidget()
        base.setLayout(layout)
        return base

    def update_index(self, row):
        index = self.findChild(QSpinBox, "index")
        index.valueChanged.disconnect()
        index.setValue(row + 1)
        index.valueChanged.connect(self._move_to)
        self.row = row

    def update_view(self):
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

        view = self.findChild(QLabel, "view")
        view.setText(self._ENTRY_VIEW.format(content=content))

    # Set the text of downloaded contents to each of matched editors
    def update_editor(self, items):
        if 'atop' in items:
            self.editors['atop'].setText(items['atop'])

        for i in range(1, self.lv1 + 1):
            if 'def-%d' % i in items:
                self.editors['def-%d' % i].setText(items['def-%d' % i])
            for j in range(1, self.lv2 + 1):
                if 'ex-%d-%d' % (i, j) in items:
                    self.editors['ex-%d-%d' % (i, j)].setText(items['ex-%d-%d' % (i, j)])

    def _move_to(self, next):
        # Converts index to row of list.count()
        next -= 1
        if next == self.row:
            # When spin.setValue triggers this method
            return

        if not 0 <= next < self.parent.count():
            spin = self.findChild(QSpinBox, "index")
            spin.setValue(self.row + 1)
        else:
            self.move.emit(self.row, next)

    def str_index(self):
        # Return string number from 00000 to 99999 based on the index
        index = self.row + 1
        snum = (5 - len(str(index))) * '0' + str(index)
        return snum

    # Returns the class' properties in a dictionary. Will be called on saving.
    def data(self):
        data = {}
        data['idx'] = self.row + 1
        data['atop'] = self.editors['atop'].text()
        data['lv1'] = self.lv1
        data['lv2'] = self.lv2
        for i in range(1, self.lv1 + 1):
            data['def-%d' % i] = self.editors['def-%d' % i].text()
            for j in range(1, self.lv2 + 1):
                data['ex-%d-%d' % (i, j)] = self.editors['ex-%d-%d' % (i, j)].text()

        return data

