import gui
from gui.qt import *


class GroupButton(QPushButton):
    def __init__(self, trigger, group=None, idx=None):
        super(GroupButton, self).__init__()
        self.trigger = trigger
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
        self.clicked.connect(lambda: self.trigger(idx=self.idx))