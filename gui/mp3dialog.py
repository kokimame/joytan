from gui.qt import *
import gui
from gui.utils import getFile, getFileNameFromPath, isLin, isMac, processCoreEvents
from tools.cmder.mp3cmder import mp3Duration, hhmmss2secCmd, getMp3Info

def onMp3Dialog(mw):
    gui.dialogs.open("Mp3Dialog", mw)


class MediaPlayer(QMediaPlayer):
    def __init__(self):
        super(MediaPlayer, self).__init__()

    def playContent(self, content):
        self.setMedia(content)
        self.play()

class Mp3Widget(QWidget):
    def __init__(self, mediaPlayer, mp3path, index, parent=None):
        super(Mp3Widget, self).__init__(parent)
        self.mp = mediaPlayer
        self.mp3path = mp3path
        self.filename = getFileNameFromPath(mp3path)
        self.hhmmss = mp3Duration(mp3path)
        self.duration, self.fskhz, self.bitkbs = getMp3Info(mp3path)
        self.index = index
        self.content = QMediaContent(QUrl.fromLocalFile(mp3path))

        self.initUi()

    def initUi(self):
        label = QLabel("{index}. {name} {hhmmss}".
                       format(index=self.index, name=self.filename, hhmmss=self.hhmmss))

        playBtn = QPushButton("Play")
        playBtn.clicked.connect(lambda: self.mp.playContent(self.content))

        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(playBtn)
        self.setLayout(hbox)



class Mp3Dialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.framelist = mw.framelist
        self.mp = MediaPlayer()
        self.form = gui.forms.mp3dialog.Ui_Mp3Dialog()
        self.form.setupUi(self)
        self.setupButton()
        self.setupComboBox()
        self.setupSfxList()
        self.setupBgmList()
        self.show()

    def setupSfxList(self):
        pass

    def setupBgmList(self):
        bgmBar = QListWidgetItem()
        addBtn = QPushButton("+ BGM")
        addBtn.setStyleSheet("QPushButton { background-color: rgb(200,200,200); "
                             "Text-align: left; }")
        addBtn.clicked.connect(self.onBgmClicked)
        bgmBar.setSizeHint(addBtn.sizeHint())
        self.form.bgmList.addItem(bgmBar)
        self.form.bgmList.setItemWidget(bgmBar, addBtn)

    def setupButton(self):
        form = self.form
        form.createBtn.clicked.connect(self.onCreate)

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


        from tools.cmder.mp3cmder import Mp3Cmder
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
            bw = self.framelist.getBundleWidget(i)
            os.makedirs("{root}/{dirname}".format(
                        root=self.mw.getRootPath(), dirname=bw.getDirname()), exist_ok=True)

            cmder.ttsBundleWidget(bw)
            pdcnt += 1
            pd.setValue(pdcnt)
            processCoreEvents()

            cmder.compileBundle(bw, isGstatic=isGstatic)
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
            assert os.path.isdir(file) != True
            lw, w = QListWidgetItem(), Mp3Widget(self.mp, file, list.count())
            lw.setSizeHint(w.sizeHint())
            list.addItem(lw)
            list.setItemWidget(lw, w)
        except (IndexError, AssertionError):
            print("Invalid file is selected.")
            pass


    def reject(self):
        self.done(0)
        gui.dialogs.close("Mp3Dialog")