
from gui.qt import *
from gui.bundle import BundleFactory

class FrameList(QListWidget):

    def __init__(self, parent=None):
        super(FrameList, self).__init__(parent)
        self.bf = BundleFactory()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)

    def updateBundle(self, name, items):
        for bw in self.getCurrentBundleWidgets():
            if bw.name == name:
                bw.updateEditors(items)
                return
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)


    def addBundle(self, name, mode):
        if name == '': pass
        elif name in [bw.name for bw in self.getCurrentBundleWidgets()]:
            print("Bundle with name %s already exists." % name)
            return

        bui, bw = self.bf.createUi(self.count() + 1, name, mode, parent=self)
        self.addItem(bui)
        self.setItemWidget(bui, bw)

    def deleteBundle(self):
        for bui in self.selectedItems():
            bw = self.itemWidget(bui)
            self.takeItem(bw.index - 1)
            self.updateIndex(bw.index - 1)

    def updateIndex(self, n):
        # Update index of bundles after Nth bundle
        for i in range(n, self.count()):
            bw = self.getBundleWidget(i)
            bw.index -= 1

    def _update(self):
        # Update the inside of the bundles in the list
        print("Bundle updates")
        for i in range(self.count()):
            bui = self.item(i)
            bw = self.itemWidget(bui)
            bw.updateDisplay()
            bui.setSizeHint(bw.sizeHint())

        self.repaint()

    def updateMode(self, newMode):
        for bw in self.getCurrentBundleWidgets():
            bw.updateMode(newMode)


    def getCurrentBundleWidgets(self):
        return [self.getBundleWidget(i) for i in range(self.count())]

    def getBundleWidget(self, index):
        return self.itemWidget(self.item(index))