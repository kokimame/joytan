
from gui.qt import *
from gui.bundle import BundleFactory
# TODO: Move Bundle class into gui.bundle
from bavl.bundle import Bundle

# TODO: Rename to Frame
class FrameList(QListWidget):

    def __init__(self, parent=None):
        super(FrameList, self).__init__(parent)
        self.bf = BundleFactory()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)

    def add(self, name):
        if name in self.getCurrentNames():
            print("Bundle with name %s already exists." % name)
            return
        self.addBundle(Bundle(name, self.count() + 1))

    def updateBundle(self, name, items):
        for bundle in self.getCurrentBundles():
            if bundle.name == name:
                bundle.updateItems(items)
                return
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)


    def addBundle(self, bundle):
        bui, bitem = self.bf.createUi(self.count() + 1, bundle, parent=self)
        self.addItem(bui)
        self.setItemWidget(bui, bitem)

    def deleteSelectedUi(self):
        for bui in self.selectedItems():
            bitem = self.itemWidget(bui)
            self.takeItem(bitem.index - 1)
            self.updateIndex(bitem.index - 1)

    def updateIndex(self, n):
        # Update index of bundles after Nth bundle
        for i in range(n, self.count()):
            bitem = self.getWidgetItem(i)
            bitem.index -= 1
            bitem.updateIndex()

    def _update(self):
        # Update the inside of the bundles in the list
        print("Bundle updates")
        for i in range(self.count()):
            bui = self.item(i)
            bitem = self.itemWidget(bui)
            bitem.updateUi()
            bui.setSizeHint(bitem.sizeHint())

        self.repaint()

    def updateMode(self, newMode):
        for i in range(self.count()):
            bitem = self.getWidgetItem(i)
            bitem.updateMode(newMode)

    def getCurrentNames(self):
        return [self.getWidgetItem(i).name for i in range(self.count())]

    def getCurrentBundles(self):
        return [self.getWidgetItem(i).bundle for i in range(self.count())]


    def getWidgetItem(self, num):
        return self.itemWidget(self.item(num))