from gui.qt import *
import gui
from gui.utils import getFile, getFileNameFromPath, isLin, isMac, processCoreEvents
from bavl.cmder.mp3cmder import mp3Duration, hhmmss2secCmd, getMp3Info

def onMp3Dialog(mw):
    gui.dialogs.open("Mp3Setting", mw, mw.framelist)

class SfxTableItem(QTableWidgetItem):
    def __init__(self, parent=None):
        super(SfxTableItem, self).__init__(parent)
        self.sfxpath = None
        self.sfxname = None

    def setPath(self, path):
        self.sfxpath = path
        self.sfxname = getFileNameFromPath(path)


class BgmListItem(QListWidgetItem):
    def __init__(self, bgmpath, parent=None):
        super(BgmListItem, self).__init__(parent)
        self.bgmpath = bgmpath
        self.bgmname = getFileNameFromPath(bgmpath)
        self.duration = mp3Duration(self.bgmpath)

# TODO: Name change to Mp3Dialog
class Mp3Setting(QDialog):
    def __init__(self, mw, framelist):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.fm = mw.fm
        self.framelist = framelist
        self.form = gui.forms.mp3dialog.Ui_Mp3Dialog()
        self.form.setupUi(self)
        self.setupButton()
        self.setupSfxTable()
        self.setupComboBox()

        self.show()

    # Fixme: UI setup is too messy!
    def setupSfxTable(self):
        column = ["Set with", "Sound Effect"]
        row = ["Word", "Definitions", "Examples"]
        table = self.form.sfxTable
        table.setColumnCount(2)
        table.setRowCount(3)

        for n in range(len(column)):
            for m in range(3):
                newitem = SfxTableItem()
                if n == 0:
                    newitem.setText(row[m])
                table.setItem(m, n, newitem)


        table.itemClicked.connect(self.onSfxClicked)
        table.setHorizontalHeaderLabels(column)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        table.setColumnWidth(0, 90)
        table.setColumnWidth(1, table.width() - 120)
        [table.setRowHeight(i, 25) for i in range(3)]


    def setupButton(self):
        form = self.form
        form.createBtn.clicked.connect(self.onCreate)
        form.bgmAddBtn.clicked.connect(self.onBgmClicked)

    def setupComboBox(self):
        form = self.form
        if isMac:
            form.ttsCombo.setCurrentIndex(0)
        if isLin:
            form.ttsCombo.setCurrentIndex(1)

    def onCreate(self):
        form = self.form
        setting = {}
        setting['repeat'] = form.wordSpin.value()

        sfxdir = {}
        for i, group in enumerate(['word', 'definitions', 'examples']):
            path = form.sfxTable.item(i, 1).sfxpath
            duration, fskhz, bitkbs = getMp3Info(path)
            sfxdir[group] = {"path": path,
                             "filename": getFileNameFromPath(path),
                             "duration": duration,
                             "sampling": fskhz,
                             "bitrate": bitkbs,
                             }
        setting['sfx'] = sfxdir

        bgmloop = []
        for i in range(form.bgmList.count()):
            item = form.bgmList.item(i)
            duration, fskhz, bitkbs = getMp3Info(item.bgmpath)
            bgmloop.append({"path": item.bgmpath,
                            "filename": getFileNameFromPath(item.bgmpath),
                            "duration": duration,
                            "sampling": fskhz,
                            "bitrate": bitkbs,})
        setting['loop'] = bgmloop

        from bavl.cmder.mp3cmder import Mp3Cmder
        from gui.progress import ProgressDialog

        # Fixme: Here is the wrong progress length assumption!
        pd = ProgressDialog(self.framelist.count() * 3, msg="Creating MP3...")
        pdcnt = 0
        pd.show()

        # Setting up the properties of audio files such as bitrate and sampling rate
        cmder = Mp3Cmder(self.fm.getRootPath(), setting)

        # Fixme: Only use bundles shown in the framelist of the main window,
        # i.e. Remove getAllBundles, WYSIWYG!
        # TODO: Thus no need to pass FM but should pass a ref to framelist ui

        for i in range(self.framelist.count()):
            bitem = self.framelist.getWidgetItem(i)
            cmder.ttsBitem(bitem)
            pdcnt += 1
            pd.setValue(pdcnt)
            processCoreEvents()

        for id in self.framelist.currentIds:
            cmder.compileBundle(id)
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
                        dir=self.fm.pref['bgmdir'], filter="*.mp3")
            item = BgmListItem(file)
            row = list.count() + 1
            item.setText("%3d. %s: %s" % (row, item.duration, item.bgmname))
            list.addItem(item)
        except IndexError:
            print("Index Error passed")
            pass


    def onSfxClicked(self, item):
        row, col = item.row(), item.column()
        if col == 1:
            try:
                file = getFile(self.mw, "Select Sound effect",
                       dir=self.fm.pref['sfxdir'], filter="*.mp3")
                item.setPath(file)
                item.setText(item.sfxname)
            except IndexError:
                print("Index error passed")
                pass

    def reject(self):
        self.done(0)
        gui.dialogs.close("Mp3Setting")