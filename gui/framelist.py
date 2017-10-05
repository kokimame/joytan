
from gui.qt import *
from gui.bundle import BundleItemUi, BundleUi

class FrameList(QListWidget):

    def __init__(self, fm, parent=None):
        super(FrameList, self).__init__(parent)
        self.fm = fm
        # Store the ID of bundles whicn the UI is rendering
        # Fixme: For now, the ID is just the name of bundle but should be like hash
        self.currentIds = []

    def setNewBundles(self):
        # Check newly created bundles in the frame of the FrameManager
        newbds = self.fm.getNewBundles(self.currentIds)

        for bundle in newbds:
            bdUi, bditUi = BundleUi(), BundleItemUi(self.fm.pref, bundle)
            bdUi.setSizeHint(bditUi.sizeHint())
            self.addItem(bdUi)
            self.setItemWidget(bdUi, bditUi)
        self.setNewIds(newbds)
        print(newbds)


    def updateBundles(self):
        # Update the inside of the bundles in the list
        print("Bundle updates")
        for i in range(self.count()):
            bditUi = self.itemWidget(self.item(i))
            bditUi.updateEditors()


    def updateItem(self, Item):
        pass

    def setNewIds(self, newbds):
        for bundle in newbds:
            self.currentIds.append(bundle.name)


    def add(self, item, widget):
        pass

    def remove(self):
        pass