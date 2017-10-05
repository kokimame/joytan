# -*- coding: utf-8 -*-
# Copyright: Koki Mametani <kokimametani@gmail.com>
#
# Checking core requirements

import sys

if sys.version_info[0] < 3:
    raise Exception("Bavl requires Python 3.x")

if sys.getfilesystemencoding().lower() in ("ascii", "ansi_x3.4-1968"):
    raise Exception("Bavl requires a UTF-8 locale.")

# build scripts grep this line, so keep this format
version = "0.0.1beta1"