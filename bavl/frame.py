from gui.utils import isMac, isLin, isWin
from bavl.utils import mkdir, rmdir
from bavl.bundle import Bundle

class _Frame():
    def __init__(self):
        pass

class FrameManager():
    def __init__(self):
        # Private. Don't access Frame directly from the outside of FrameManager
        # Frame is merely a built-in list for now.
        # In future, the list may be extended to a new class.
        self._Frame = []
        self.pref = self.getPreferences()
        print(self.pref)

        # Fixme: Set this None initially and use system preference
        self.targetDict = "dictionary-com"

        # These url will be set through Preferences
        self.dictURLs = {
            "dictionary-com": "http://dictionary.com/browse/",
            "cambridge": "http://dictionary.cambridge.org/dictionary/english/",
            "oxford": "https://en.oxforddictionaries.com/definition/",
            "wiktionary": "https://en.wiktionary.org/wiki/"
        }

        rmdir(self.getRootPath())
        #self.createWorkspace()

    def initBundle(self, name, index):
        # Do some setup for bundles using "Frame preference"
        # before its initialization
        if name in self.getBundleNames():
            raise Exception("Exception: Bundle with name %s already exists." % name)
        return Bundle(name, index)

    def setBitemByName(self, name, bitem):
        for bundle in self._Frame:
            if bundle.name == name:
                bundle.updateItems(bitem)
                return
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)

    def setBundleUpdateState(self, bundle, state):
        for b in self._Frame:
            if b == bundle:
                bundle.isUpdated = state

    def addBundle(self, name):
        index = self.getFrameLength() + 1
        try:
            b = self.initBundle(name, index)
            self._Frame.append(b)
            mkdir(self.getRootPath() + '/' + name)
        except Exception as e:
            print(e)
            return

    def getRootPath(self):
        return self.pref['workdir'] + '/' + self.pref['title']


    def getPreferences(self):
        # Get setting of frame e.g. numbers of def and ex required etc
        if isLin:
            return {
                "workdir": "/home/kokimame/Emotan/workspace",
                "sfxdir": "/home/kokimame/Dropbox/Python/bavl/templates/sfx",
                "worddir": "/home/kokimame/Dropbox/Python/bavl/templates/wordlist",
                "bgmdir": "/home/kokimame/Dropbox/Python/bavl/templates/song",
                "title": "word50-gre",
                "dpb": 2, # Definition per bundle
                "epd": 1,  # Examples per definition
                "synonym": 0
            }
        elif isMac:
            return {
                "workdir": "/Users/Koki/Emotan/workspace",
                "sfxdir": "/Users/Koki/Dropbox/Python/bavl/templates/sfx",
                "worddir": "/Users/Koki/Dropbox/Python/bavl/templates/wordlist",
                "bgmdir": "/Users/Koki/Dropbox/Python/bavl/templates/song",
                "title": "word50-gre",
                "dpb": 2, # Definition to be saved in a bundle
                "epd": 1,  # Examples per definition
                "synonym": 0
            }
        elif isWin:
            raise Exception("Windows ver is now under development.")

    def printFrame(self):
        print(self._Frame)

    #def createFrameDirs(self):
    #   root = self.getRootPath()
    #    mkdir(root)
    #    for bundle in self._Frame:
    #        mkdir(root + '/' + bundle.name)
    #    print("Frame Dirs created")

    def createWorkspace(self):
        mkdir(self.pref['workdir'])


    def loadSetting(self):
        pass

    def updateSetting(self):
        pass

    def getBundlesToRender(self):
        return [b for b in self._Frame if b.toRender]

    def setToRenderState(self, bundle, state):
        bundle.toRender = state

    def getAllBundles(self):
        return [b for b in self._Frame]

    def getBundleNames(self):
        return [bundle.name for bundle in self._Frame]

    def getFrameLength(self):
        return len(self._Frame)
