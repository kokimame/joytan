
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
        for bundle in self.getCurrentBundles():
            if bundle.name == name:
                bundle.updateItems(items)
                return
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)


    def addBundle(self, name, mode):
        if name == '': pass
        elif name in self.getCurrentNames():
            print("Bundle with name %s already exists." % name)
            return

        bundle = self.bf.makeBundle(name, self.count() + 1)
        bui, bw = self.bf.createUi(self.count() + 1, bundle, mode, parent=self)
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
            bw.saveEditors()

    def _update(self):
        # Update the inside of the bundles in the list
        print("Bundle updates")
        for i in range(self.count()):
            bui = self.item(i)
            bw = self.itemWidget(bui)
            bw.updateUi()
            bui.setSizeHint(bw.sizeHint())

        self.repaint()

    def updateMode(self, newMode):
        for i in range(self.count()):
            bw = self.getBundleWidget(i)
            bw.updateMode(newMode)

    def saveEditingResult(self):
        for i in range(self.count()):
            bw = self.getBundleWidget(i)
            bw.saveEditors()

    def getCurrentNames(self):
        return [self.getBundleWidget(i).bundle.name for i in range(self.count())]

    def getCurrentBundles(self):
        return [self.getBundleWidget(i).bundle for i in range(self.count())]


    def getBundleWidget(self, num):
        return self.itemWidget(self.item(num))