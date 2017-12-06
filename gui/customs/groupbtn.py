import gui
from gui.qt import *
from gui.utils import getFile


class GroupButton(QPushButton):
    sig = pyqtSignal(str, str, int)

    def __init__(self, mw, group, dir, idx=0, filter=".mp3", msg='Select a file'):
        super(GroupButton, self).__init__()
        self.mw = mw
        self.group = group
        self.idx = idx
        self.filter = filter
        self.dir = dir
        self.msg = msg
        self.initUi()

    def initUi(self):
        self.setStyleSheet("QPushButton { background-color: rgb(200,200,200); "
                             "Text-align: left; }")
        if not self.group.isupper():
            group = self.group.title()
        else:
            group = self.group
        self.setText("+ {group}".format(group=group))
        self.clicked.connect(self.selectFile)

    def selectFile(self):
        try:
            file = getFile(self.mw, self.msg,
                        dir=self.dir, filter=self.filter)
            assert os.path.isdir(file) != True

            self.sig.emit(file, self.group, self.idx)
        except (IndexError, AssertionError, TypeError):
            print("Error: Invalid file is selected.")
            pass