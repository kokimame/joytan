import shutil
import tempfile
from contextlib import contextmanager

import sys
from warnings import warn

sys.path.insert(0, 'joytan_root')

import gui
from gui import _run


@contextmanager
def joytan_running():
    mw = _run(exec=False)
    yield mw