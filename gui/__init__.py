"""

Building and initializing GUI of .
The entire PyQt programming pattern is learned from Anki project
(https://github.com/dae/anki)

"""
import optparse
import tempfile

from gui.qt import *
from gui.utils import isMac, isLin, isWin

from joytan.bundle import Bundle
from joytan.config import Config
from joytan import conversion as to

# TODO: Deploy with confident. Very obscure right now
if sys.version_info[0] < 3:
    raise Exception("Joytan requires Python 3.x")

if sys.getfilesystemencoding().lower() in ("ascii", "ansi_x3.4-1968"):
    raise Exception("Joytan requires a UTF-8 locale.")

# build scripts grep this line, so keep this format
app_version = "0.0.1beta1"
# Main window set in runtime
mw = None
logger = None
config = None
ICONS = 'design/icons'

try:
    import gui.forms
except ImportError as e:
    if "forms" in str(e):
        print("Error: Build UI first by running build_ui.sh from the project root.\n")
    raise

from gui import preferences, audiodialog, textdialog, \
    download, translate, copy, extract, sort


class DialogManager:
    _dialogs = {
        "Preferences": [preferences.Preferences, None],
        "AudioDialog": [audiodialog.AudioDialog, None],
        "TextDialog": [textdialog.TextDialog, None],
        "DownloadDialog": [download.DownloadDialog, None],
        "TranslateDialog": [translate.TranslateDialog, None],
        "CopyDialog": [copy.CopyDialog, None],
        "ExtractDialog": [extract.ExtractDialog, None],
        "SortDialog": [sort.SortDialog, None],
    }

    def open(self, name, *args, **kargs):
        (creator, instance) = self._dialogs[name]
        if instance:
            if not instance.isVisible():
                instance.setVisible(True)
            instance.setWindowState(Qt.WindowNoState)
            instance.activateWindow()
            instance.raise_()
            return instance
        # if Dialog instace is new
        else:
            instance = creator(*args, **kargs)
            # Remember the newly created instance
            self._dialogs[name][1] = instance
            return instance

    def close(self, name, save=False):
        if not save:
            self._dialogs[name] = [self._dialogs[name][0], None]

dialogs = DialogManager()


class JoytanApp(QApplication):
    def __init___(self, argv):
        QApplication.__init__(self, argv)
        self._argv = argv


def parse_args(argv):
    """Returns (opts, args)"""
    if isMac and len(argv) > 1 and argv[1].startswith("-psn"):
        argv = [argv[0]]
    parser = optparse.OptionParser(version="%prog " + app_version)
    parser.usage = "%prog [OPTIONS] [file to import]"
    parser.add_option("-b", "--base", help="path to base folder")
    parser.add_option("-l", "--lang", help="interface language (en, de, etc)")
    return parser.parse_args(argv[1:])


def run():
    try:
        _run()
    except Exception as e:
        QMessageBox.critical(None, "Startup Error",
                             "Please notify support of this error:\n\n"+
                             traceback.format_exc())


def _run(argv=None, exec=True):
    """
    Start JoytanApp application or reuse an exisiting instance if one exits.
    
    If the function isi invoked with exec=False, the JoytanApp will not enter
    the main event loop, instead the application object will be returned
    
    The 'exec' and 'argv' is useful for testing purposes
    """
    global mw, app

    opts, args = parse_args(sys.argv)
    opts.base = opts.base or ""

    app = JoytanApp(sys.argv)
    QCoreApplication.setApplicationName("Joytan ジョイ単")

    # disable icons on mac; this must be done before window created
    if isMac:
        app.setAttribute(Qt.AA_DontShowIconsInMenus)

    # work around pyqt loading wrong GL library
    if isLin:
        import ctypes
        ctypes.CDLL('libGL.so.1', ctypes.RTLD_GLOBAL)

    # we must have a usable temp dir
    try:
        tempfile.gettempdir()
    except:
        QMessageBox.critical(
            None, "Error", """\
        No usable temporary folder found. Make sure C:\\temp exists or TEMP in your \
        environment points to a valid, writable folder.""")
        return

    global logger, config

    logger = Bundle(debug=lambda *a, **k: None, error=lambda *a, **k: None,
                    info=lambda *a, **k: None, warn=lambda *a, **k: None)

    config = Config(
        db=Bundle(base=opts.base,
                  table='general',
                  normalize=to.normalized_ascii),
        cols=[
            ('extras', 'text', {}, to.deserialized_dict, to.compact_json),
            ('filenames', 'text', 'hash', str, str),
            ('filenames_human', 'text',
             '{{text}} ({{service}} {{voice}})', str, str),
            ('groups', 'text', {}, to.deserialized_dict, to.compact_json),
            ('lame_flags', 'text', '--quiet -q 2', str, str),
            ('last_options', 'text', {}, to.deserialized_dict, to.compact_json),
            ('last_service', 'text', ('sapi5js' if 'win32' in sys.platform
                                      else 'say' if 'darwin' in sys.platform
            else 'espeak'), str, str),
            ('presets', 'text', {}, to.deserialized_dict, to.compact_json),
        ],
        logger=logger,
        events=[
        ],
    )

    import gui.main
    mw = gui.main.JoytanMW(app, sys.argv)
    if exec:
        app.exec_()
    else:
        return mw
