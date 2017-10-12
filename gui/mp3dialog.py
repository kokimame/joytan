from gui.qt import *
import gui
from gui.utils import getFile, getFileNameFromPath, isLin, isMac, processCoreEvents
from bavl.cmder.mp3cmder import mp3Duration, hhmmss2secCmd, getMp3Info

def onMp3Dialog(mw):
    gui.dialogs.open("Mp3Setting", mw, mw.framelist)


class Mp3ListItem(QListWidgetItem):
    def __init__(self, mp3path, parent=None):
        super(Mp3ListItem, self).__init__(parent)
        self.mp3path = mp3path
        self.filename = getFileNameFromPath(mp3path)
        self.hhmmss = mp3Duration(mp3path)
        self.duration, self.fskhz, self.bitkbs = getMp3Info(mp3path)

class Mp3TreeItem(QTreeWidgetItem):
    def __init__(self, mp3path, parent=None):
        super(Mp3TreeItem, self).__init__(parent)
        self.mp3path = mp3path
        self.filename = getFileNameFromPath(mp3path)
        self.hhmmss = mp3Duration(mp3path)
        self.duration, self.fskhz, self.bitkbs = getMp3Info(mp3path)


# TODO: Name change to Mp3Dialog
class Mp3Setting(QDialog):
    def __init__(self, mw, framelist):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = framelist
        self.form = gui.forms.mp3dialog.Ui_Mp3Dialog()
        self.form.setupUi(self)
        self.setupButton()
        self.setupComboBox()
        self.setupSfxTree()
        self.show()

    def setupSfxTree(self):
        tree = self.form.sfxTree
        tree.itemClicked.connect(self.onSfxClicked)
        self.sfxGroup = []

        for group in ['Word', 'Definition', 'Example']:
            groupItem = QTreeWidgetItem(tree)
            groupItem.setExpanded(True)
            groupItem.setText(0, group)
            self.sfxGroup.append(groupItem)


    def setupButton(self):
        form = self.form
        form.createBtn.clicked.connect(self.onCreate)
        form.addBgmBtn.clicked.connect(self.onBgmClicked)

    def setupComboBox(self):
        form = self.form
        if isMac:
            form.ttsCombo.setCurrentIndex(0)
        if isLin:
            form.ttsCombo.setCurrentIndex(1)

    def onCreate(self):
        form = self.form
        isGstatic = form.gstaticCheck.isChecked()
        setting = {}
        setting['repeat'] = form.wordSpin.value()

        sfxdir = {}
        for item in self.sfxGroup:
            # SFXs for a group shown in column 0
            group = item.text(0)
            sfxdir[group] = []
            for i in range(item.childCount()):
                child = item.child(i)
                sfxdir[group].append({
                    "path": child.mp3path,
                    "filename": child.filename,
                    "duration": child.duration,
                    "sampling": child.fskhz,
                    "bitrate": child.bitkbs
                })
        setting['sfx'] = sfxdir

        bgmloop = []
        for i in range(form.bgmList.count()):
            item = form.bgmList.item(i)
            bgmloop.append({"path": item.mp3path,
                            "filename": item.filename,
                            "duration": item.duration,
                            "sampling": item.fskhz,
                            "bitrate": item.bitkbs,})
        setting['loop'] = bgmloop


        from bavl.cmder.mp3cmder import Mp3Cmder
        from gui.progress import ProgressDialog

        # Fixme: Here is the wrong progress length assumption!
        pd = ProgressDialog(self.framelist.count() * 3, msg="Creating MP3...")
        pdcnt = 0
        pd.show()

        # Setting up the properties of audio files such as bitrate and sampling rate
        cmder = Mp3Cmder(self.mw.getRootPath(), setting)

        # Fixme: Only use bundles shown in the framelist of the main window,
        # i.e. Remove getAllBundles, WYSIWYG!
        # TODO: Thus no need to pass FM but should pass a ref to framelist ui

        for i in range(self.framelist.count()):
            bitem = self.framelist.getWidgetItem(i)
            os.makedirs("{root}/{dirname}".format(
                        root=self.mw.getRootPath(), dirname=bitem.getDirname()), exist_ok=True)

            cmder.ttsBitem(bitem)
            pdcnt += 1
            pd.setValue(pdcnt)
            processCoreEvents()

            cmder.compileBundle(bitem, isGstatic=isGstatic)
            pdcnt += 1
            pd.setValue(pdcnt)
            processCoreEvents()

        cmder.mergeDirMp3()
        cmder.createBgmLoop()

        # Fixme: More preciously define the progress out of TTS session
        pdcnt += int(self.framelist.count() / 2)
        pd.setValue(pdcnt)
        processCoreEvents()

        cmder.mixWithBgm()

        self.reject()

    def onBgmClicked(self):
        list = self.form.bgmList
        try:
            file = getFile(self.mw, "Add song to BGM Loop",
                        dir=self.mw.pref['bgmdir'], filter="*.mp3")
            item = Mp3ListItem(file)
            row = list.count() + 1
            item.setText("%3d. %s: %s" % (row, item.hhmmss, item.filename))
            list.addItem(item)
        except IndexError:
            print("Index Error passed")
            pass


    def onSfxClicked(self, item, column):
        if item.text(0) == '': return
        try:
            file = getFile(self.mw, "Chose a SFX",
                        dir=self.mw.pref['sfxdir'], filter="*.mp3")
            child = Mp3TreeItem(file, parent=item)
            child.setText(1, child.filename)
            child.setText(2, child.hhmmss)
            item.addChild(child)

        except IndexError:
            print("Index Error passed")
            pass

    def reject(self):
        self.done(0)
        gui.dialogs.close("Mp3Setting")