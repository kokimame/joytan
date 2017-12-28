import gui
from gui.qt import *
from gui.utils import getFile


class FileSelector(QPushButton):
    select = pyqtSignal(str, int)

    def __init__(self, mw, group, dir, idx=0, filter="*.mp3", msg='Select a file'):
        super(FileSelector, self).__init__()
        self.mw = mw
        self.group = group
        self.idx = idx
        self.filter = filter
        self.dir = dir
        self.msg = msg
        self._ui()

    def _ui(self):
        self.setStyleSheet("QPushButton { background-color: rgb(200,200,200); "
                           "Text-align: left; }")

        self.setText("+ {group}".format(group=self.group))
        self.clicked.connect(self._on_file_select)

    def _on_file_select(self):
        try:
            file = getFile(self.mw, self.msg, dir=self.dir, filter=self.filter)
            self.select.emit(file, self.idx)
        except:
            return

