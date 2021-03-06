# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html
#
# ===========================================
# Several classes and methods with CamelCase are copied from Anki project.
# These components are distributed under the same licence shown below.
#
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import sip
import os

# fixme: buggy ubuntu12.04 display of language selector
os.environ["LIBOVERLAY_SCROLLBAR"] = "0"

from PyQt5.Qt import *
from PyQt5.QtMultimedia import QMediaPlayer
# trigger explicit message in case of missing libraries
# insted of silently failing to import


def debug():
    from PyQt5.QtCore import pyqtRemoveInputHook
    from pdb import set_trace
    pyqtRemoveInputHook()
    set_trace()

import sys, traceback

if os.environ.get("DEBUG"):
    def info(type, value, tb):
        from PyQt5.QtCore import pyqtRemoveInputHook
        for line in traceback.format_exception(type, value, tb):
            sys.stdout.write(line)
        pyqtRemoveInputHook()
        from pdb import pm
        pm()
    sys.excepthook = info


# Check Qt Version requirement
qtmajor = (QT_VERSION & 0xff0000) >> 16
qtminor = (QT_VERSION & 0x00ff00) >> 8
qtpoint = QT_VERSION & 0xff