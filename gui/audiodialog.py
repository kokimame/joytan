import shutil

import gui
from gui.qt import *
from gui.utils import showCritical, getFiles
from gui.widgets.flowitem import FlowItem, Mp3Object, EwkeyObject, Rest, Index


def on_audiodialog(mw):
    gui.dialogs.open("AudioDialog", mw)


class AudioDialog(QDialog):

    def __init__(self, mw):
        QDialog.__init__(self, mw, Qt.Window)
        self.mw = mw
        self.thread = None
        self.form = gui.forms.audiodialog.Ui_AudioDialog()
        self.form.setupUi(self)

        self.list_lookup = {
            'flow': dict(
                ui=self.form.flowList,
                col='sfxdir',
                msg='Select sound effect',
            ),
            'bgm': dict(
                ui=self.form.bgmList,
                col='bgmdir',
                msg='Select BGM',
            )
        }
        self._ui_button()
        self._ui_progress()
        self._ui_add_flow()
        self._ui_add_bgm()

        self.show()

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

    def _ui_add_flow(self):
        fadd = self.form.flowAdd
        fadd.clicked.connect(self._flow_tool)
        fadd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        fadd.setArrowType(Qt.DownArrow)

        self._add_item(self.list_lookup['flow'], Index)
        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            self._add_item(self.list_lookup['flow'], EwkeyObject, ewkey)

    def _ui_add_bgm(self):
        badd = self.form.bgmAdd
        badd.clicked.connect(self._bgm_tool)
        badd.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        badd.setArrowType(Qt.DownArrow)

    def _flow_tool(self):
        m = QMenu(self.mw)
        a = m.addAction("Add Sound effect")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['flow'], Mp3Object))
        a = m.addAction("Add Rest")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['flow'], Rest))
        a = m.addAction("Add Index")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['flow'], Index))
        for ewkey in self.mw.entrylist.get_config('ewkeys'):
            a = m.addAction("Add %s" % ewkey)
            a.triggered.connect(lambda ignore, key=ewkey:
                                self._add_item(self.list_lookup['flow'], EwkeyObject, key))
        m.exec_(QCursor.pos())

    def _bgm_tool(self):
        m = QMenu(self.mw)
        a = m.addAction("Add Song")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['bgm'], Mp3Object))
        a = m.addAction("Add Rest")
        a.triggered.connect(lambda: self._add_item(self.list_lookup['bgm'], Rest))
        m.exec_(QCursor.pos())

    def _add_item(self, lookup, cls, *args):
        # Type may spawn multiple flow item
        if cls is Mp3Object:
            try:
                files = getFiles(self.mw, lookup['msg'],
                                 dir=self.mw.config[lookup['col']], filter="*.mp3")
            except:
                return

            for file in files:
                lwi = QListWidgetItem()
                fi = cls(file)
                lwi.setSizeHint(fi.sizeHint())
                fi.delete.connect(lambda base=lookup['ui'], item=lwi: self._remove_item(base, item))
                lookup['ui'].addItem(lwi)
                lookup['ui'].setItemWidget(lwi, fi)
            return
        # ======================
        # Types for single flow item
        lwi = QListWidgetItem()
        fi = cls(*args)
        lwi.setSizeHint(fi.sizeHint())
        fi.delete.connect(lambda base=lookup['ui'], item=lwi: self._remove_item(base, item))

        lookup['ui'].addItem(lwi)
        lookup['ui'].setItemWidget(lwi, fi)

    def _remove_item(self, _list, lwi):
        for i in range(_list.count()):
            if lwi == _list.item(i):
                _list.takeItem(i)

    def _on_create(self):
        el = self.mw.entrylist
        if el.count() == 0:
            showCritical("No entries found in your entry list.")
            return

        setting = {}
        setting['title'] = self.mw.config['title']
        # TODO: Is it safe to return copied object from el?
        setting['ttsmap'] = el.get_config('ttsmap').copy()

        # Open TTS setting dialog if TTS is not allocated to
        _list = self.form.flowList
        undefs = el.get_config('undefined')
        for i in range(_list.count()):
            fi = _list.itemWidget(_list.item(i))
            if isinstance(fi, EwkeyObject) and fi.ewkey in undefs:
                showCritical("Please choose Text-to-speech voice for each of Entry section to be read.")
                gui.dialogs.open("Preferences", self.mw, back_to=self, tab="TTS")
                return
        # Safe to pop out ewkeys to which TTS voice is undefined but unused in audiobook
        for key in undefs:
            setting['ttsmap'].pop(key, None)


        destdir = os.path.join(self.mw.projectbase(), "audio")
        if os.path.isdir(destdir):
            shutil.rmtree(destdir)
        setting['dest'] = destdir

        # Check if LRC file needs to be created
        setting['lrc'] = self.form.lrcCheck.isChecked()

        _list = self.form.flowList
        flow = []
        for i in range(_list.count()):
            fi = _list.itemWidget(_list.item(i))
            assert isinstance(fi, FlowItem)
            flow.append(fi.data())

        setting['flow'] = flow

        _list = self.form.bgmList
        loop = []
        for i in range(_list.count()):
            fi = _list.itemWidget(_list.item(i))
            assert isinstance(fi, FlowItem)
            loop.append(fi.data())

        setting['loop'] = loop

        finalpath = os.path.join(setting['dest'], setting['title'])

        class Mp3HandlerThread(QThread):
            prog = pyqtSignal(str)
            fail = pyqtSignal(str)

            def __init__(self, mw, handler):
                QThread.__init__(self)
                self.mw = mw
                self.handler = handler

            def run(self):
                self.prog.emit("Setting up aufio files. This may take a few minutes")
                self.handler.setup_audio()
                for i in range(el.count()):
                    ew = el.get_entry_at(i)
                    self.prog.emit("Creating audio file of %s." % ew['atop'])
                    os.makedirs(os.path.join(destdir, ew.str_index()), exist_ok=True)
                    try:
                        self.handler.onepass(ew)
                    except Exception as e:
                        self.fail.emit("Error occurs while processing audio files. System stops "
                                       "at exception '%s'" % e)
                        self.terminate()

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

        def _on_fail(msg):
            showCritical(msg)
            
        self.thread = Mp3HandlerThread(self.mw, handler)
        self.thread.prog.connect(_on_progress)
        self.thread.fail.connect(_on_fail)
        self.thread.start()
        self.form.createBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        self.thread.finished.connect(self._init_progress)

    def _on_stop_thread(self):
        if self.thread:
            self.thread.terminate()
            destdir = os.path.join(self.mw.projectbase(), "audio")
            shutil.rmtree(destdir)
            self.form.progressBar.reset()
            self.form.pgMsg.setText("")
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)

    def _stop_all_audio(self):
        for _list in [self.form.flowList, self.form.bgmList]:
            for i in range(_list.count()):
                iw = _list.itemWidget(_list.item(i))
                if isinstance(iw, Mp3Object):
                    iw.force_stop()

    def _init_progress(self):
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")

    def reject(self):
        self._init_progress()
        self._stop_all_audio()
        self.done(0)
        gui.dialogs.close("AudioDialog")
