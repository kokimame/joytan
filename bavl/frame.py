from gui.utils import isMac, isLin, isWin
from bavl.utils import mkdir, rmdir
from bavl.bundle import Bundle

class _Frame():
    def __init__(self):
        pass

class FrameManager():
    def __init__(self, mw):
        # Private. Don't access Frame directly from the outside of FrameManager
        # Frame is merely a built-in list for now.
        # In future, the list may be extended to a new class.
        self._Frame = []
        self.mw = mw

        rmdir(self.mw.getRootPath())

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
