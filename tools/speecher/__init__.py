# -*- coding: utf-8 -*-
# Copyright: Koki Mametani <kokimametani@gmail.com>
#
import os
from subprocess import call, check_output

from gui.utils import isWin


class BaseSpeecher:
    def dictate(self, script, langCode=None, output=None):
        raise NotImplementedError

    def save(self, script, output, langCode=None):
        raise NotImplementedError

    def isSupported(self):
        raise NotImplementedError


from tools.speecher.say import Say
from tools.speecher.espeak import Espeak

# Interfaces for various text-to-speech application
Speechers = {
    "say": Say,
    "espeak": Espeak,
}