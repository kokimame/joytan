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

        # Fixme: Set this None initially and use system preference
        self.targetDict = "dictionary-com"

        # These url will be set through Preferences
        self.dictURLs = {
            "dictionary-com": "http://dictionary.com/browse/",
            "cambridge": "http://dictionary.cambridge.org/dictionary/english/",
            "oxford": "https://en.oxforddictionaries.com/definition/",
            "wiktionary": "https://en.wiktionary.org/wiki/"
        }

        if isLin:
            self.pref = {
                "workdir": "/home/kokimame/Emotan/workspace",
                "sfxdir": "/home/kokimame/Dropbox/Python/emotan/templates/sfx",
                "worddir": "/home/kokimame/Dropbox/Python/emotan/templates/wordlist",
                "bgmdir": "/home/kokimame/Dropbox/Python/emotan/templates/song",
                "title": "word50-gre",
                "synonym": 0
            }
        elif isMac:
            self.pref = {
                "workdir": "/Users/Koki/Emotan/workspace",
                "sfxdir": "/Users/Koki/Dropbox/Python/emotan/templates/sfx",
                "worddir": "/Users/Koki/Dropbox/Python/emotan/templates/wordlist",
                "bgmdir": "/Users/Koki/Dropbox/Python/emotan/templates/song",
                "title": "word50-gre",
                "synonym": 0
            }
        else:
            print("Sorry, Windows is now under development!")

        print(self.pref)

        rmdir(self.getRootPath())

    def initBundle(self, name, index):
        # Do some setup for bundles using "Frame preference"
        # before its initialization
        if name in self.getBundleNames():
            raise Exception("Exception: Bundle with name %s already exists." % name)
        return Bundle(name, index)

    # This should be done by ID not name
    def setBitemByName(self, name, bitem):
        for bundle in self._Frame:
            if bundle.name == name:
                bundle.updateItems(bitem)
                return
        raise Exception("Error: Bundle with name '%s' is not found in the Frame" % name)


    def addBundle(self, name):
        index = self.getFrameSize() + 1
        try:
            b = self.initBundle(name, index)
            self._Frame.append(b)
            mkdir(self.getRootPath() + '/' + name)
        except Exception as e:
            print(e)
            return

    def getRootPath(self):
        return self.pref['workdir'] + '/' + self.pref['title']

    def getNewBundles(self, ids):
        newbds = []
        for bundle in self._Frame:
            if bundle.name not in ids:
                newbds.append(bundle)
        return newbds

    def createWorkspace(self):
        mkdir(self.pref['workdir'])


    # TODO: Delete the method
    # FrameManager only accepts requests for a part of bundles from other components
    # Don't give them all of it to manage bundles by their own.
    def getAllBundles(self):
        return [b for b in self._Frame]

    def getBundleNames(self):
        return [bundle.name for bundle in self._Frame]

    def getFrameSize(self):
        return len(self._Frame)
