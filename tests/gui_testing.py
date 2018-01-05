import os
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
    # Configure output directory for testing
    test_argv = ["-t", "--test", os.path.join(os.getcwd(), 'tests')]
    mw = _run(argv=test_argv, exec=False)
    yield mw
    # If there's nothing to do after yield gets called,
    # is yield equivalent to return?