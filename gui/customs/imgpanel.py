import gui
from gui.qt import *

class ImagePanel(QListWidget):
    def __init__(self):
        super(ImagePanel, self).__init__()
        self.setFlow(QListView.LeftToRight)
