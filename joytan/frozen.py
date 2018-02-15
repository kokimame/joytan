# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

# Path to bundled binary file of dependency libraries.
# These files will be accessed at run-time when the app is "frozen".
# NOTE:
# The installed Linux application is not recognized as "frozen" as
# the bundled app on the other OS be.
# Currently Linux users download the dependencies by themselves.
# It can be done easily by `sudo apt-get install {lame and ffmpeg}`
import os
import sys

FROZEN_FFMPEG = os.path.join(os.path.dirname(sys.executable), "ffmpeg")
FROZEN_LAME = os.path.join(os.path.dirname(sys.executable), "lame")
FROZEN_TEXTBOOK = os.path.join(os.path.dirname(sys.executable), "default_textbook.html")