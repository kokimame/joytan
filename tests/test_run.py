import os
import json

from gui.widgets.entrylist import EntryList
from .gui_testing import joytan_running

def test_entrylist():
    with joytan_running() as mw:
        ew1 = mw.entrylist.add_entry('test1', mw.mode)
        ew2 = mw.entrylist.add_entry('test2', mw.mode)
        ew3 = mw.entrylist.add_entry('test3', mw.mode)

        # Count after adding 3 Entry
        assert mw.entrylist.count() == 3

        # Remove Entry with atop 'test1'
        mw.entrylist._remove_at(0)
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
        mw.entrylist.remove_all()
        assert mw.entrylist.count() == 0


def test_open():
    # Sample Joytan EntryList file to open
    test_jel = 'tests/assets/en_en.jel'
    assert os.path.exists(test_jel), 'Test file %s not found' % test_jel

    with joytan_running() as mw:
        from gui.open import on_open
        on_open(mw, file=test_jel)

        assert mw.entrylist.count() == 4
        assert not mw.entrylist.get_config('voiceless')

        # Atop key is in ewkeys
        assert 'atop' in mw.entrylist.get_config('ewkeys')
        lv1 = mw.entrylist.get_config('lv1')
        lv2 = mw.entrylist.get_config('lv2')

        # Number of ewkeys: atop + def-n * (ex-n-m + 1)
        n_keys = 1 + lv1 * (lv2 + 1)
        assert n_keys == len(mw.entrylist.get_config('ewkeys'))
