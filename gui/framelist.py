
from gui.qt import *
from gui.bundle import BundleItemUi, BundleUi

# TODO: Move Bundle class into gui.bundle
from bavl.bundle import Bundle

# TODO: Rename to Frame
class FrameList(QListWidget):

    class FrameManager():
        def initBundle(self, name, names, index):
            # Do some setup for bundles using "Frame preference"
            # before its initialization
            if name in names:
                raise Exception("Exception: Bundle with name %s already exists." % name)
            return Bundle(name, index)

        # This should be done by ID not name
        def setItemByName(self, name, item):
            for bundle in self._Frame:
                if bundle.name == name:
                    bundle.updateItems(item)
                    return
            raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)

        def remove(self, bundle):
            self._Frame.remove(bundle)

        def getBundleNames(self):
            return [bundle.name for bundle in self._Frame]


    def __init__(self, mw, parent=None):
        super(FrameList, self).__init__(parent)
        self.mw = mw
        self.fm = FrameList.FrameManager()
        # Fixme: Framelist become frame itself. No need to store ids
        self.currentIds = []
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setStyleSheet("""
                            QListWidget::item { border-bottom: 1px solid black; }
                            QListWidget::item:selected { background: rgba(0,255,255,30); }
                           """)

    def updateItem(self, Item):
        pass

    def add(self, name):
        if name in self.getCurrentNames():
            raise Exception("Exception: Bundle with name %s already exists." % name)
        self.addBundle(Bundle(name, self.count() + 1))


    def remove(self):
        pass

    def addBundle(self, bundle):
        bui, bitem = self.mw.bdfactory.createUi(self.count() + 1, bundle, parent=self)
        self.addItem(bui)
        self.setItemWidget(bui, bitem)
        # Fixme: Use real ID to check existing bundles in the list
        self.setNewId(bundle.name)

    def setNewBundles(self):
        # TODO: Move FM out of the class and make two classes communicate with each other(?)
        # TODO: Or delete FM class at all and make FrameList do everything.
        # like Signal & Slot (?)
        # Check newly created bundles in the frame of the FrameManager
        newbds = self.fm.getNewBundles(self.currentIds)

        for bundle in newbds:
            self.addBundle(bundle)


    def deleteSelectedUi(self):
        for bui in self.selectedItems():
            bitem = self.itemWidget(bui)
            self.takeItem(bitem.index - 1)
            self.currentIds.remove(bitem.name)
            self.fm.remove(bitem.bundle)
            self.updateIndex(bitem.index - 1)

    def updateIndex(self, n):
        # Update index of bundles after Nth bundle
        for i in range(n, self.count()):
            bitem = self.getWidgetItem(i)
            bitem.index -= 1
            bitem.updateIndex()

    def updateBundles(self):
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

    def setNewId(self, id):
        self.currentIds.append(id)

    def getCurrentNames(self):
        return [self.getWidgetItem(i).name for i in range(self.count())]


    def getWidgetItem(self, num):
        return self.itemWidget(self.item(num))