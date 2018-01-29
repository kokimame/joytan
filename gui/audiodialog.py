# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

import shutil
import pydub

import gui
from gui.qt import *
from gui.utils import showCritical, getFiles, getCompleted
from gui.widgets.flowitem import FlowItem, Mp3Object, EwkeyObject, Rest, Index


def on_audiodialog(mw):
    # Check if the user install dependencies for pydub
    if not pydub.utils.which("ffmpeg") and not pydub.utils.which("libav"):
        showCritical("Error: Dependecies not found. "
                     "Please install 'ffmpeg' or 'libav' to create audiobooks")
        return

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
        self._ui_spin()
        self._ui_add_flow()
        self._ui_add_bgm()

        self.show()

    def _ui_button(self):
        self.form.createBtn.clicked.connect(self._on_create)
        self.form.stopBtn.setEnabled(False)
        self.form.stopBtn.clicked.connect(self._on_stop)
        self.form.settingBtn.clicked.connect(
            lambda: gui.dialogs.open("Preferences", self.mw, back_to=self, tab="TTS"))

    def _ui_progress(self):
        self.form.progressBar.setValue(0)

    def _ui_spin(self):
        pass

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

    def _add_item(self, lookup, _class, *args):
        # Maybe spawn multiple flowitems at once, such as several SFX or BGM
        if _class is Mp3Object:
            try:
                files = getFiles(self.mw, lookup['msg'],
                                 dir=self.mw.config[lookup['col']], filter="*.mp3")
            except:
                return

            for file in files:
                lwi = QListWidgetItem()
                fi = _class(file)
                lwi.setSizeHint(fi.sizeHint())
                fi.delete.connect(lambda base=lookup['ui'], item=lwi: self._remove_item(base, item))
                lookup['ui'].addItem(lwi)
                lookup['ui'].setItemWidget(lwi, fi)
            return
        # ======================
        # Otherwise, Spawn a single flowitem, such as Rest
        lwi = QListWidgetItem()
        fi = _class(*args)
        lwi.setSizeHint(fi.sizeHint())
        fi.delete.connect(lambda base=lookup['ui'], item=lwi: self._remove_item(base, item))

        lookup['ui'].addItem(lwi)
        lookup['ui'].setItemWidget(lwi, fi)

    def _remove_item(self, _list, lwi):
        for i in range(_list.count()):
            if lwi == _list.item(i):
                _list.takeItem(i)

    def _on_create(self):
        # Validation before starting to create audiobooks
        if self.mw.entrylist.count() == 0:
            showCritical("No entries found in your entry list.")
            return

        # entries: The Entry to be included in the upcoming audiobook.
        if self.form.allBtn.isChecked():
            entries = self.mw.entrylist.get_entry_all()
        else:
            _from, _to = self.form.fromSpin.value(), self.form.toSpin.value()
            if _from > _to:
                showCritical("The value in 'to' field is out of range.")
                self._init_spin()
                return
            else:
                try:
                    entries = self.mw.entrylist.get_entry_all()[_from-1:_to]
                except IndexError:
                    showCritical("Index is out of range.")
                    self._init_spin()
                    return

        # Open TTS setting dialog if TTS setting is incomplete.
        _list = self.form.flowList
        undefs = self.mw.entrylist.get_config('undefined')
        for i in range(_list.count()):
            fi = _list.itemWidget(_list.item(i))
            if isinstance(fi, EwkeyObject) and fi.ewkey in undefs:
                showCritical("Please choose Text-to-speech voice for every Entry section to be read.")
                gui.dialogs.open("Preferences", self.mw, back_to=self, tab="TTS")
                return

        if os.path.isdir(self._destdir()):
            # When dubbing thread gets interrupted by exceptions that it fails to find dependencies
            # (e.g, ffmpeg) while creating audio files, it may leave these files, like index.mp3, open.
            # This situation causes permission error on Windows if user starts the thread again and
            # tries to remove existing folders, because some of files in the folders are in use.
            # Therefore, let's ignore errors from shutil below and let pydub raise an error later.
            shutil.rmtree(self._destdir(), ignore_errors=True)
            os.makedirs(self._destdir(), exist_ok=True)

        setting = self._get_setting()

        class DubbingThread(QThread):
            prog = pyqtSignal(str)
            fail = pyqtSignal(str)

            def __init__(self, mw, worker):
                QThread.__init__(self)
                self.mw = mw
                self.worker = worker

            def run(self):
                self.completed = False
                self.prog.emit("Setting up aufio files. This may take a few minutes")
                self.worker.setup_audio()
                for ew in entries:
                    self.prog.emit("Creating audio file of %s." % ew['atop'])
                    os.makedirs(os.path.join(setting['dest'], ew.str_index()), exist_ok=True)
                    try:
                        self.worker.onepass(ew)
                    except Exception as e:
                        self.fail.emit("Error occurs while creating audiobook. System stops "
                                       "with exception '%s'" % e)
                        self.sleep(100)

                self.prog.emit("Mixing with BGM. This may take a few minutes.")
                acapella = sum(self.worker.acapellas)
                # Is this good for memory efficiency?
                del self.worker.acapellas

                if len(setting['loop']) != 0:
                    try:
                        finalmp3 = acapella.overlay(self.worker.get_bgmloop(len(acapella)))
                        finalmp3.export(setting['dest'] + ".mp3")
                    except Exception as e:
                        self.fail.emit("Error occurs while making a looped BGM. System stops "
                                       "with exception '%s'" % e)
                else:
                    acapella.export(setting['dest'] + ".mp3")

                if setting['lrc']:
                    self.worker.make_lyrics(setting['dest'] + ".lrc")

                self.completed = True
                self.quit()

        def _on_progress(msg):
            self.form.pgMsg.setText(msg)
            val = self.form.progressBar.value()
            self.form.progressBar.setValue(val+1)

        def _on_fail(msg):
            """
            This slot gets called if the dubbing thread encounters an exception,
            then shows a critical error message and kills the thread.
            """
            if self.thread:
                self.thread.terminate()
            showCritical(msg)

        from joytan.routine.dubbing import DubbingWorker
        worker = DubbingWorker(setting)
        self.thread = DubbingThread(self.mw, worker)
        self.thread.prog.connect(_on_progress)
        self.thread.fail.connect(_on_fail)
        self.thread.start()
        self.thread.finished.connect(lambda: self._completed(setting['dest']))

        self.form.createBtn.setEnabled(False)
        self.form.stopBtn.setEnabled(True)
        # Progress contains fixed 2 step; setting up audio files, mixing with BGM
        self.form.progressBar.setRange(0, len(entries)+3)

    def _on_stop(self):
        if self.thread:
            self.thread.terminate()
            shutil.rmtree(self._destdir(), ignore_errors=True)
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

    def _completed(self, path):
        self._init_progress()
        # To debug audio elements of audiobooks, remove the line below.
        shutil.rmtree(self._destdir(), ignore_errors=True)
        if self.thread.completed:
            getCompleted(path + ".mp3")

    def _get_setting(self):
        el = self.mw.entrylist
        setting = dict()
        setting['title'] = self.mw.config['title']
        # TODO: Is it safe to return copied object from el?
        setting['ttsmap'] = el.get_config('ttsmap').copy()

        undefs = el.get_config('undefined')
        # Safe to pop out ewkeys to which TTS voice is undefined but unused in audiobook
        for key in undefs:
            setting['ttsmap'].pop(key, None)

        setting['dest'] = self._destdir()
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
        return setting

    def _destdir(self):
        return os.path.join(self.mw.projectbase(), "audiobook")

    def _init_progress(self):
        self.form.stopBtn.setEnabled(False)
        self.form.createBtn.setEnabled(True)
        self.form.progressBar.reset()
        self.form.pgMsg.setText("")

    def _init_spin(self):
        self.form.fromSpin.setValue(1)
        self.form.toSpin.setValue(1)

    def reject(self):
        self._init_progress()
        self._stop_all_audio()
        self.done(0)
        gui.dialogs.close("AudioDialog")
