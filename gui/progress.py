# -*- coding: utf-8 -*-
# This module was used in past time, but currently not in use.
# 
# Several classes and methods with CamelCase are copied from Anki project.
# These components are distributed under the same licence shown below.
# ===========================================
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import time
from gui.qt import *

class ProgressManager:
    def __init__(self, mw):
        self.mw = mw
        self.app = QApplication.instance()
        self._win = None
        self._levels = 0

    class ProgressNoCancel(QProgressDialog):
        def closeEvent(self, evt):
            evt.ignore()
        def keyPressEvent(self, evt):
            if evt.key() == Qt.Key_Escape:
                evt.ignore()

    class ProgressCancellable(QProgressDialog):
        def __init__(self, *args, **kwargs):
            QProgressDialog.__init__(self, *args, **kwargs)
            self.progCancel = False

        def closeEvent(self, evt):
            self.progCancel = True
            evt.ignore()

        def keyPressEvent(self, evt):
            if evt.key() == Qt.Key_Escape:
                evt.ignore()
                self.progCancel = True

    def start(self, min=0, max=0, label=None, parent=None, immediate=False, cancellable=False):
        self._levels += 1
        if self._levels > 1:
            return
        parent = parent or self.app.activeWindow()
        if not parent and self.mw.isVisible():
            parent = self.mw

        label = label or "Processing..."
        if cancellable:
            cls = self.ProgressCancellable
        else:
            cls = self.ProgressNoCancel

        self._win = cls(label, "", min, max, parent)
        self._win.setWindowTitle("Joytan")
        self._win.setCancelButton(None)
        self._win.setAutoClose(False)
        self._win.setAutoReset(False)
        self._win.setMinimumWidth(300)

        if immediate:
            self._showWin()
        else:
            self._shown = False

        self._counter = min
        self._min = min
        self._max = max
        self._firstTime = time.time()
        self._lastUpdate = time.time()
        self._updating = False
        return self._win

    def update(self, label=None, value=None, step=None, process=True, maybeShow=True):
        if self._updating:
            return
        if maybeShow:
            self._maybeShow()
        elapsed = time.time() - self._lastUpdate
        if label:
            self._win.setLabelText(label)
        if self._max and self._shown:
            assert not (value and step), "Error: Cannot use custom value and step at once."
            if step:
                self._counter = self._counter + step
            else:
                self._counter = value or (self._counter+1)
            self._win.setValue(self._counter)
        if process and elapsed >= 0.2:
            self._updating = True
            self.app.processEvents(QEventLoop.ExcludeUserInputEvents)
            self._updating = False
            self._lastUpdate = time.time()

    def finish(self):
        self._levels -= 1
        self._levels = max(0, self._levels)
        if self._levels == 0 and self._win:
            self._closeWin()

    def clear(self):
        if self._levels:
            self._levels = 1
            self.finish()

    def _maybeShow(self):
        if not self._levels:
            return
        if self._shown:
            self.update(maybeShow=False)
            return

        delta = time.time() - self._firstTime
        if delta > 0.5:
            self._showWin()

    def _showWin(self):
        self._shown = time.time()
        self._win.show()
        self._setBusy()

    def _closeWin(self):
        if self._shown:
            while True:
                delta = time.time() - self._shown
                if delta >= 0.5:
                    break
                self.app.processEvents(QEventLoop.ExcludeUserInputEvents)
        self._win.cancel()
        self._unsetBusy()

    def _setBusy(self):
        self.mw.app.setOverrideCursor(QCursor(Qt.WaitCursor))

    def _unsetBusy(self):
        self.app.restoreOverrideCursor()

    def busy(self):
        return self._levels

