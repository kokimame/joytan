# Copyright: Koki Mametani <kokimametani@gmail.com>

from gui.qt import *

if sys.version_info[0] < 3:
    raise Exception("Emotan requires Python 3.x")

if sys.getfilesystemencoding().lower() in ("ascii", "ansi_x3.4-1968"):
    raise Exception("Emotan requires a UTF-8 locale.")

# build scripts grep this line, so keep this format
appVersion = "0.0.1beta1"

mw = None # Main window set in runtime

moduleDir = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

try:
    import gui.forms
except ImportError as e:
    if "forms" in str(e):
        print("Error: Build UI first by running build_ui.sh from the project root.\n")
    raise


from gui import preferences, mp3dialog, textdialog, download, translate, langdetect

class DialogManager:
    _dialogs = {
        "Preferences": [preferences.Preferences, None],
        "Mp3Dialog": [mp3dialog.Mp3Dialog, None],
        "TextDialog": [textdialog.TextDialog, None],
        "DownloadDialog": [download.DownloadDialog, None],
        "TranslateDialog": [translate.TranslateDialog, None],
        "LangDetectDialog": [langdetect.LangDetectDialog, None]
    }

    def open(self, name, *args, **kargs):
        (creator, instance) = self._dialogs[name]
        if instance:
            instance.setWindowState(Qt.WindowNoState)
            instance.activateWindow()
            instance.raise_()
            return instance
        else: # if Dialog instace is new
            instance = creator(*args, **kargs)
            # Remember the newly created instance
            self._dialogs[name][1] = instance
            return instance

    def close(self, name):
        self._dialogs[name] = [self._dialogs[name][0], None]

dialogs = DialogManager()


class EmotanApp(QApplication):
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
    global mw, app# Main window
    print("Run the GUI")

    app = EmotanApp(sys.argv)
    QCoreApplication.setApplicationName("Emotan")

    import gui.main
    mw = gui.main.EmotanMW(app, sys.argv)
    app.exec_()