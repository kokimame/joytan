import gui
from gui.qt import *
from gui.utils import getFile


class GroupButton(QPushButton):
    sig = pyqtSignal(str, str, int)

    def __init__(self, mw, group, idx=0):
        super(GroupButton, self).__init__()
        self.mw = mw
        self.group = group
        self.idx = idx
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
        if self.group != "BGM":
            msg = "Add sound effect to %s" % self.group
            dir = self.mw.setting['sfxdir']
        else:
            msg = "Add song to BGM Loop"
            dir = self.mw.setting['bgmdir']
        try:
            file = getFile(self.mw, msg,
                        dir=dir, filter="*.mp3")
            assert os.path.isdir(file) != True

            self.sig.emit(file, self.group, self.idx)
        except (IndexError, AssertionError, TypeError):
            print("Error: Invalid file is selected.")
            pass