# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

"""
Building and initializing GUI.

Acknowledgement:
PyQt programming pattern is based on Anki project
(https://github.com/dae/anki)
"""

import optparse
import tempfile

from gui.qt import *
from gui.utils import isMac, isLin, isWin, defaultWorkspace, defaultMusic, defaultDocument

from joytan.bundle import Bundle
from joytan.config import Config
from joytan import conversion as to


if sys.version_info[0] < 3:
    raise Exception("Joytan requires Python 3.x")

if sys.getfilesystemencoding().lower() in ("ascii", "ansi_x3.4-1968"):
    raise Exception("Joytan requires a UTF-8 locale.")

# build scripts grep this line, so keep this format
app_version = "0.2.0"
# Main window set in runtime
mw = None
logger = None
config = None

try:
    import gui.forms
except ImportError as e:
    if "forms" in str(e):
        print("Error: Build UI first by running build_ui.sh from the project root.\n")
    raise

from gui import preferences, audiodialog, textdialog, \
    lookup, translate, copy, sort, open, memrise


class DialogManager:
    _dialogs = {
        "Preferences": [preferences.Preferences, None],
        "AudioDialog": [audiodialog.AudioDialog, None],
        "TextDialog": [textdialog.TextDialog, None],
        "LookupDialog": [lookup.LookupDialog, None],
        "TranslateDialog": [translate.TranslateDialog, None],
        "CopyDialog": [copy.CopyDialog, None],
        "SortDialog": [sort.SortDialog, None],
        "OpenDialog": [open.OpenDialog, None],
        "MemriseDialog": [memrise.MemriseDialog, None],
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
    parser.add_option("-t", "--test", help="output directory for (py)testing")
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
    Start JoytanApp application or reuse an existing instance if one exits.
    
    If the function ii invoked with exec=False, the JoytanApp will not enter
    the main event loop, instead the application object will be returned
    
    The 'exec' and 'argv' is useful for testing purposes
    """
    global app

    if argv is None:
        argv = sys.argv

    # Parse args
    opts, args = parse_args(argv)
    opts.base = opts.base or ""

    app = JoytanApp(sys.argv)
    QCoreApplication.setApplicationName("Joytan")

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
            ('title', 'text', 'joytan-sample', str, str),
            ('workspace', 'text', defaultWorkspace(), str, str),
            ('bgmdir', 'text', defaultMusic(), str, str),
            ('sfxdir', 'text', defaultMusic(), str, str),
            ('worddir', 'text', defaultDocument(), str, str),
            ('last_workspace', 'text', defaultWorkspace(), str, str),
            ('last_bgmdir', 'text', defaultMusic(), str, str),
            ('last_sfxdir', 'text', defaultMusic(), str, str),
            ('last_worddir', 'text', defaultDocument(), str, str),
            ('extras', 'text', {}, to.deserialized_dict, to.compact_json),
            ('filenames', 'text', 'hash', str, str),
            ('filenames_human', 'text',
             '{{text}} ({{service}} {{voice}})', str, str),
            ('groups', 'text', {}, to.deserialized_dict, to.compact_json),
            ('lame_flags', 'text', '--quiet -q 2', str, str),
            ('last_options', 'text', {}, to.deserialized_dict, to.compact_json),
            ('last_service', 'text', ('sapi5com' if 'win32' in sys.platform
                                      else 'say' if 'darwin' in sys.platform
                                      else 'espeak'), str, str),
            ('presets', 'text', {}, to.deserialized_dict, to.compact_json),
        ],
        logger=logger,
        events=[
        ],
    )

    # TODO: Separate config.db for testing and running
    if opts.test:
        config['workspace'] = opts.test
    else:
        config['workspace'] = defaultWorkspace()


    global mw
    import gui.main
    print("Hi Windows users, don't close this black window. Sorry for your inconvenience.\n"
          "Without this window, the audiobook feature cannot work on Windows because of an technical issue.\n"
          "This will be fixed in the future!")
    mw = gui.main.JoytanMW(app, config, sys.argv)
    if exec:
        app.exec_()
    else:
        return mw
