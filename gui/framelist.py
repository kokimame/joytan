
from gui.qt import *
from gui.bundle import BundleItemUi, BundleUi

class FrameList(QListWidget):

    def __init__(self, mw, parent=None):
        super(FrameList, self).__init__(parent)
        self.mw = mw
        self.fm = mw.fm
        # Store the ID of bundles whicn the UI is rendering
        # Fixme: For now, the ID is just the name of bundle but should be like hash
        self.currentIds = []
        self.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")

    def setNewBundles(self):
        # TODO: Move FM out of the class and make two classes communicate with each other(?)
        # TODO: Or delete FM class at all and make FrameList do everything.
        # like Signal & Slot (?)
        # Check newly created bundles in the frame of the FrameManager
        newbds = self.fm.getNewBundles(self.currentIds)

        for bundle in newbds:
            self.addBundle(bundle)

    def addBundle(self, bundle):
        bui, bitem = self.mw.bdfactory.createUi(self.count() + 1, bundle, parent=self)
        self.addItem(bui)
        self.setItemWidget(bui, bitem)
        # Fixme: Use real ID to check existing bundles in the list
        self.setNewId(bundle.name)

    def deleteUi(self, ui):
        self.takeItem(ui.index - 1)
        self.currentIds.remove(ui.name)
        self.fm.remove(ui.bundle)
        self.updateIndex(ui.index - 1)

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


    def setNewId(self, id):
        self.currentIds.append(id)

    def getWidgetItem(self, num):
        return self.itemWidget(self.item(num))

    def updateItem(self, Item):
        pass

    def add(self, item, widget):
        pass

    def remove(self):
        pass