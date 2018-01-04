import os
import json

from gui.widgets.entrylist import EntryList
from .gui_testing import joytan_running


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
