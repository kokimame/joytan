from gui.utils import isMac, isLin, isWin
from bavl.bundle import Bundle

class FrameManager():

    def initBundle(self, name, index):
        # Do some setup for bundles using "Frame preference"
        # before its initialization
        if name in self.getBundleNames():
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


    def add(self, name):
        index = self.getFrameSize() + 1
        try:
            b = self.initBundle(name, index)
            self._Frame.append(b)
        except Exception as e:
            print(e)
            return

    def getNewBundles(self, ids):
        newbds = []
        for bundle in self._Frame:
            if bundle.name not in ids:
                newbds.append(bundle)
        return newbds

    def getBundleNames(self):
        return [bundle.name for bundle in self._Frame]

    def getFrameSize(self):
        return len(self._Frame)
