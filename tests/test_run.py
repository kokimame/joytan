# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Kohki Mametani <kohkimametani@gmail.com>
# License: GNU GPL version 3 or later; http://www.gnu.org/licenses/gpl.html

import os
import shutil
import json

from gui.widgets.entrylist import EntryList
from .gui_testing import joytan_running


def test_entrylist():
    with joytan_running() as mw:
        # Initially entrylist shows one helper list item telling basic usages
        assert super(EntryList, mw.entrylist).count() == 1
        # But it's ignored on application level
        assert mw.entrylist.count() == 0

        ew1 = mw.entrylist.add_entry(atop='test1')
        ew2 = mw.entrylist.add_entry(atop='test2')
        ew3 = mw.entrylist.add_entry(atop='test3')

        # Count after adding 3 Entry
        assert mw.entrylist.count() == 3

        # Remove Entry with atop 'test1'
        mw.entrylist._remove_entry_at(0)
        assert mw.entrylist.count() == 2

        # Test get_entry_at
        ew_2_test = mw.entrylist.get_entry_at(0)
        ew_3_test = mw.entrylist.get_entry_at(1)
        assert ew2 == ew_2_test
        assert ew3 == ew_3_test

        # Check if main mode affects Entry mode
        assert ew_2_test.mode == 'View'
        mw._on_mode_update()
        assert ew_2_test.mode == 'Edit'

        # Test remove_all
        mw.entrylist.remove_entry_all()
        assert mw.entrylist.count() == 0
