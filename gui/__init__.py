# Copyright: Koki Mametani <kokimametani@gmail.com>

from bavl import version as _version

import getpass
import sys
import optparse
import tempfile
import builtins
import locale
import gettext

from gui.qt import *

appVersion = _version
mw = None # Main window set in runtime

moduleDir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

try:
    import gui.forms
except ImportError as e:
    if "forms" in str(e):
        print("Error: Build UI first by running build_ui.sh from the project root.\n")
    raise


from gui import preferences, mp3dialog

class DialogManager:
    _dialogs = {
        "Preferences": [preferences.Preferences, None],
        "Mp3Setting": [mp3dialog.Mp3Setting, None]
    }

    def open(self, name, *args):
        (creator, instance) = self._dialogs[name]
        if instance:
            instance.setWindowState(Qt.WindowNoState)
            instance.activateWindow()
            instance.raise_()
            return instance
        else: # if Dialog instace is new
            instance = creator(*args)
            # Remember the newly created instance
            self._dialogs[name][1] = instance
            return instance

    def close(self, name):
        self._dialogs[name] = [self._dialogs[name][0], None]

dialogs = DialogManager()


class BavlApp(QApplication):
    def __init___(self, argv):
        QApplication.__init__(self, argv)
        self._argv = argv


def parseArgs(argv):
    pass

def run():
    try:
        _run()
    except Exception as e:
        QMessageBox.critical(None, "Startup Error")

def _run():
    global mw, app # Main window
    print("Run the GUI")

    app = BavlApp(sys.argv)
    QCoreApplication.setApplicationName("Emotan")

    import gui.main
    mw = gui.main.BavlMW(app, sys.argv)
    app.exec_()