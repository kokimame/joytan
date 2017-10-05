from gui.qt import *

class ProgressDialog(QProgressDialog):
    def __init__(self, end, start=0, msg="Please wait..."):
        QProgressDialog.__init__(self)
        self.setRange(start, end)
        self.setValue(start)
        self.setWindowModality(Qt.WindowModal)
        self.canceled.connect(self.close)
        self.setCancelButtonText("Stop")
        self.setWindowTitle(msg)