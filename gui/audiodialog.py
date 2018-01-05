import shutil

import gui
from gui.qt import *
from gui.utils import showCritical, getFiles
from gui.widgets.flowitem import FlowItem, Mp3Object, EwkeyObject, Silence


def on_audiodialog(mw):
    gui.dialogs.open("AudioDialog", mw)


class AudioDialog(QDialog):
    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.thread = None
        self.form = gui.forms.audiodialog.Ui_AudioDialog()
        self.form.setupUi(self)
        self._ui_button()
        self._ui_flow()
        self._ui_bgmloop()
        self._ui_progress()
        self.show()

    def _ui_flow(self):
        fadd = self.form.flowAdd
        fadd.clicked.connect(self._flow_tool)
        fadd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        fadd.setArrowType(Qt.DownArrow)

        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            self._add_flow_item(ewkey)

    def _flow_tool(self):
        m = QMenu(self.mw)
        a = m.addAction("Add Sound effect")
        a.triggered.connect(lambda: self._add_flow_item("MP3"))
        a = m.addAction("Add Silence")
        a.triggered.connect(lambda: self._add_flow_item("SIL"))
        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            a = m.addAction("Add %s" % ewkey)
            a.triggered.connect(lambda ignore, type=ewkey: self._add_flow_item(type))
        m.exec_(QCursor.pos())

    def _ui_bgmloop(self):
        badd = self.form.bgmAdd
        badd.clicked.connect(self._bgm_tool)
        badd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        badd.setArrowType(Qt.DownArrow)

    def _bgm_tool(self):
        m = QMenu(self.mw)
        a = m.addAction("Add Song")
        a.triggered.connect(lambda: self._add_bgm("MP3"))
        a = m.addAction("Add Silence")
        a.triggered.connect(lambda: self._add_bgm("SIL"))
        m.exec_(QCursor.pos())

    def _add_flow_item(self, type):
        lwi = None
        fi = None

        # Type may spawn multiple flow item
        if type == 'MP3':
            try:
                files = getFiles(self.mw, "Select sound effect",
                                 dir=self.mw.config['sfxdir'], filter="*.mp3")
            except:
                return

            for file in files:
                lwi = QListWidgetItem()
                fi = Mp3Object(lwi, file)
                lwi.setSizeHint(fi.sizeHint())
                fi.delete.connect(self._remove_flow_item)
                self.form.flowList.addItem(lwi)
                self.form.flowList.setItemWidget(lwi, fi)
            return

        # Types for single flow item
        elif type == 'SIL':
            lwi = QListWidgetItem()
            fi = Silence(lwi)
        else:
            assert type in self.mw.entrylist.get_config('ewkeys')
            lwi = QListWidgetItem()
            fi = EwkeyObject(lwi, type)

        lwi.setSizeHint(fi.sizeHint())
        fi.delete.connect(self._remove_flow_item)
        self.form.flowList.addItem(lwi)
        self.form.flowList.setItemWidget(lwi, fi)

    def _add_bgm(self, type):
        lwi = None
        fi = None
        # Type may spawn multiple flow item
        if type == 'MP3':
            try:
                files = getFiles(self.mw, "Select sound effect",
                                 dir=self.mw.config['bgmdir'], filter="*.mp3")
            except Exception as e:
                print(e)
                return
            for file in files:
                lwi = QListWidgetItem()
                fi = Mp3Object(lwi, file)
                lwi.setSizeHint(fi.sizeHint())
                fi.delete.connect(self._remove_bgm)
                self.form.bgmList.addItem(lwi)
                self.form.bgmList.setItemWidget(lwi, fi)
            return

        # Type for single flow item
        elif type == 'SIL':
            lwi = QListWidgetItem()
            fi = Silence(lwi)
            lwi.setSizeHint(fi.sizeHint())
            fi.delete.connect(self._remove_bgm)
            self.form.bgmList.addItem(lwi)
            self.form.bgmList.setItemWidget(lwi, fi)

    def _remove_flow_item(self, lwi):
        _list = self.form.flowList
        for i in range(_list.count()):
            if lwi == _list.item(i):
                _list.takeItem(i)

    def _remove_bgm(self, lwi):
        _list = self.form.bgmList
        for i in range(_list.count()):
            if lwi == _list.item(i):
                _list.takeItem(i)

    def _ui_button(self):
        form = self.form
        form.createBtn.clicked.connect(self._on_create)
        form.stopBtn.setEnabled(False)
        form.stopBtn.clicked.connect(self._on_stop_thread)
        form.settingBtn.clicked.connect(
            lambda: gui.dialogs.open("Preferences", self.mw, back_to=self, tab="TTS"))

    def _ui_progress(self):
        form = self.form
        form.progressBar.setValue(0)

    def _on_create(self):
        el = self.mw.entrylist
        if el.count() == 0:
            showCritical("No entries found in your entry list.")
            return

        # Open TTS setting dialog if TTS is not allocated to
        # all of EntryWidget's text editor
        if el.get_config('voiceless'):
            showCritical("Please set TTS voice to all section")
            gui.dialogs.open("Preferences", self.mw, tab="ATTS")
            return

        setting = {}
        setting['title'] = self.mw.config['title']
        setting['ttsmap'] = el.get_config('ttsmap')

        destdir = os.path.join(self.mw.projectbase(), "audio")
        if os.path.isdir(destdir):
            shutil.rmtree(destdir)
        setting['dest'] = destdir

        # Check if LRC file needs to be created
        setting['lrc'] = self.form.lrcCheck.isChecked()
        # Check if index needs to be read in the output
        setting['idx'] = self.form.idxCheck.isChecked()

        flow = self.form.flowList
        flowlist = []
        for i in range(flow.count()):
            fi = flow.itemWidget(flow.item(i))
            assert isinstance(fi, FlowItem)
            if isinstance(fi, Mp3Object):
                flowlist.append({"type": "MP3",
                                 "path": fi.mp3path,
                                 "volume": fi.mp.volume()})
            elif isinstance(fi, Silence):
                flowlist.append({"type": "SIL",
                                 "duration": fi.get_duration()})
            elif isinstance(fi, EwkeyObject):
                flowlist.append({"type": fi.ewkey})
        setting['flow'] = flowlist

        bgms = self.form.bgmList
        bgmloop = []

        for i in range(bgms.count()):
            fi = bgms.itemWidget(bgms.item(i))
            assert isinstance(fi, FlowItem)
            if isinstance(fi, Mp3Object):
                bgmloop.append({"type": "MP3",
                                "path": fi.mp3path,
                                "volume": fi.mp.volume()})
            elif isinstance(fi, Silence):
                bgmloop.append({"type": "SIL",
                                "duration": fi.get_duration()})
        setting['loop'] = bgmloop

        finalpath = os.path.join(setting['dest'], setting['title'])

        class Mp3HandlerThread(QThread):
            prog = pyqtSignal(str)

            def __init__(self, mw, handler):
                QThread.__init__(self)
                self.mw = mw
                self.handler = handler

            def run(self):
                self.prog.emit("Setting up aufio files. This may take a few minutes")
                self.handler.setup_audio()
                for i in range(el.count()):
                    ew = el.get_entry_at(i)
                    self.prog.emit("Creating audio file of %s." % ew.editors['atop'].text())
                    os.makedirs(os.path.join(destdir, ew.str_index()), exist_ok=True)
                    self.handler.onepass(ew)

                self.prog.emit("Mixing with BGM. This may take a few minutes.")
                acapella = sum(self.handler.acapellas)
                if len(setting['loop']) != 0:
                    finalmp3 = acapella.overlay(self.handler.get_bgmloop(len(acapella)))
                    finalmp3.export(finalpath + ".mp3")
                else:
                    acapella.export(finalpath + ".mp3")

                if setting['lrc']:
                    self.handler.write_lyrics(finalpath + ".lrc")

                self.quit()

        from joytan.handler.mp3handler import Mp3Handler
        handler = Mp3Handler(setting)
        self.form.progressBar.setRange(0, el.count()+3)

        def _on_progress(msg):
            self.form.pgMsg.setText(msg)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)
            
        self.thread = Mp3HandlerThread(self.mw, handler)
        self.thread.prog.connect(_on_progress)
        self.thread.start()
        self.form.createBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        self.thread.finished.connect(self.reject)

    def _on_stop_thread(self):
        if self.thread:
            self.thread.terminate()
            destdir = os.path.join(self.mw.projectbase(), "audio")
            shutil.rmtree(destdir)
            self.form.progressBar.reset()
            self.form.pgMsg.setText("")
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)

    def stop_all_audio(self):
        for _list in [self.form.flowList, self.form.bgmList]:
            for i in range(_list.count()):
                iw = _list.itemWidget(_list.item(i))
                if isinstance(iw, Mp3Object):
                    iw.force_stop()

    def reject(self):
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")
        self.stop_all_audio()
        self.done(0)
        gui.dialogs.close("AudioDialog")
