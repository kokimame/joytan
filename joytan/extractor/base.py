# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GPLv3 or later; http://www.gnu.org/licenses/gpl.html

class Extractor:
    def __init__(self, file):
        self.file = file

    def run(self):
        # Extractor's result should be completely independent from the application
        # This means the input is only a file and output is the list of words in the file.
        # Implementation of the run with underscore depends on file formats
        ret = self._run()
        # Verify the behaviour of subclasses
        assert type(ret) is list
        return ret


    def _run(self):
        # Return the list of words in a given file with a specific format.
        # The run with underscore is only called from the base's run method
        raise NotImplementedError