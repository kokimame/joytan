# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
# Copyright (C) 2010-Present  Anki AwesomeTTS Development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Add-on package initialization
"""

from os.path import join
import sys
from time import time

from PyQt5.QtCore import PYQT_VERSION_STR, Qt
from PyQt5.QtGui import QKeySequence

import emotan
from . import paths, service
from emotan import conversion as to
from emotan.bundle import Bundle
from emotan.config import Config
from .router import Router

__all__ = ['browser_menus', 'cards_button', 'config_menu', 'editor_button',
           'reviewer_hooks', 'sound_tag_delays', 'update_checker',
           'window_shortcuts']


def get_platform_info():
    """Exception-tolerant platform information for use with AGENT."""

    implementation = system_description = "???"
    python_version = "?.?.?"

    try:
        import platform
    except:  # catch-all, pylint:disable=bare-except
        pass
    else:
        try:
            implementation = platform.python_implementation()
        except:  # catch-all, pylint:disable=bare-except
            pass

        try:
            python_version = platform.python_version()
        except:  # catch-all, pylint:disable=bare-except
            pass

        try:
            system_description = platform.platform().replace('-', ' ')
        except:  # catch-all, pylint:disable=bare-except
            pass

    return "%s %s; %s" % (implementation, python_version, system_description)

VERSION = '1.13.0-dev'

WEB = 'https://ankiatts.appspot.com'

AGENT = 'AwesomeTTS/%s (Anki %s; PyQt %s; %s)' % (VERSION, 'Emotan version',
                                                  PYQT_VERSION_STR,
                                                  get_platform_info())


# Begin core class initialization and dependency setup, pylint:disable=C0103

logger = Bundle(debug=lambda *a, **k: None, error=lambda *a, **k: None,
                info=lambda *a, **k: None, warn=lambda *a, **k: None)
# for logging output, replace `logger` with a real one, e.g.:
# import logging as logger
# logger.basicConfig(stream=sys.stdout, level=logger.DEBUG)

sequences = {key: QKeySequence()
             for key in ['browser_generator', 'browser_stripper',
                         'configurator', 'editor_generator', 'templater']}

config = Config(
    db=Bundle(path=emotan.CONFIG,
              table='general',
              normalize=to.normalized_ascii),
    cols=[
        ('automaticAnswers', 'integer', True, to.lax_bool, int),
        ('automatic_answers_errors', 'integer', True, to.lax_bool, int),
        ('automaticQuestions', 'integer', True, to.lax_bool, int),
        ('automatic_questions_errors', 'integer', True, to.lax_bool, int),
        ('cache_days', 'integer', 365, int, int),
        ('delay_answers_onthefly', 'integer', 0, int, int),
        ('delay_answers_stored_ours', 'integer', 0, int, int),
        ('delay_answers_stored_theirs', 'integer', 0, int, int),
        ('delay_questions_onthefly', 'integer', 0, int, int),
        ('delay_questions_stored_ours', 'integer', 0, int, int),
        ('delay_questions_stored_theirs', 'integer', 0, int, int),
        ('ellip_note_newlines', 'integer', False, to.lax_bool, int),
        ('ellip_template_newlines', 'integer', False, to.lax_bool, int),
        ('extras', 'text', {}, to.deserialized_dict, to.compact_json),
        ('filenames', 'text', 'hash', str, str),
        ('filenames_human', 'text',
         '{{text}} ({{service}} {{voice}})', str, str),
        ('groups', 'text', {}, to.deserialized_dict, to.compact_json),
        ('lame_flags', 'text', '--quiet -q 2', str, str),
        ('last_mass_append', 'integer', True, to.lax_bool, int),
        ('last_mass_behavior', 'integer', True, to.lax_bool, int),
        ('last_mass_dest', 'text', 'Back', str, str),
        ('last_mass_source', 'text', 'Front', str, str),
        ('last_options', 'text', {}, to.deserialized_dict, to.compact_json),
        ('last_service', 'text', ('sapi5js' if 'win32' in sys.platform
                                  else 'say' if 'darwin' in sys.platform
                                  else 'yandex'), str, str),
        ('last_strip_mode', 'text', 'ours', str, str),
        ('launch_browser_generator', 'integer', Qt.ControlModifier | Qt.Key_T,
         to.nullable_key, to.nullable_int),
        ('launch_browser_stripper', 'integer', None, to.nullable_key,
         to.nullable_int),
        ('launch_configurator', 'integer', Qt.ControlModifier | Qt.Key_T,
         to.nullable_key, to.nullable_int),
        ('launch_editor_generator', 'integer', Qt.ControlModifier | Qt.Key_T,
         to.nullable_key, to.nullable_int),
        ('launch_templater', 'integer', Qt.ControlModifier | Qt.Key_T,
         to.nullable_key, to.nullable_int),
        ('otf_only_revealed_cloze', 'integer', False, to.lax_bool, int),
        ('otf_remove_hints', 'integer', False, to.lax_bool, int),
        ('presets', 'text', {}, to.deserialized_dict, to.compact_json),
        ('spec_note_count', 'text', '', str, str),
        ('spec_note_count_wrap', 'integer', True, to.lax_bool, int),
        ('spec_note_ellipsize', 'text', '', str, str),
        ('spec_note_strip', 'text', '', str, str),
        ('spec_template_count', 'text', '', str, str),
        ('spec_template_count_wrap', 'integer', True, to.lax_bool, int),
        ('spec_template_ellipsize', 'text', '', str, str),
        ('spec_template_strip', 'text', '', str, str),
        ('strip_note_braces', 'integer', False, to.lax_bool, int),
        ('strip_note_brackets', 'integer', False, to.lax_bool, int),
        ('strip_note_parens', 'integer', False, to.lax_bool, int),
        ('strip_template_braces', 'integer', False, to.lax_bool, int),
        ('strip_template_brackets', 'integer', False, to.lax_bool, int),
        ('strip_template_parens', 'integer', False, to.lax_bool, int),
        ('sub_note_cloze', 'text', 'anki', str, str),
        ('sub_template_cloze', 'text', 'anki', str, str),
        ('sul_note', 'text', [], to.substitution_list, to.substitution_json),
        ('sul_template', 'text', [], to.substitution_list,
         to.substitution_json),
        ('templater_cloze', 'integer', True, to.lax_bool, int),
        ('templater_field', 'text', 'Front', str, str),
        ('templater_hide', 'text', 'normal', str, str),
        ('templater_target', 'text', 'front', str, str),
        ('throttle_sleep', 'integer', 30, int, int),
        ('throttle_threshold', 'integer', 10, int, int),
        ('TTS_KEY_A', 'integer', Qt.Key_F4, to.nullable_key, to.nullable_int),
        ('TTS_KEY_Q', 'integer', Qt.Key_F3, to.nullable_key, to.nullable_int),
        ('updates_enabled', 'integer', True, to.lax_bool, int),
        ('updates_ignore', 'text', '', str, str),
        ('updates_postpone', 'integer', 0, int, lambda i: int(round(i))),
    ],
    logger=logger,
    events=[
    ],
)


router = Router(
    services=Bundle(
        mappings=[
            ('abair', service.Abair),
            ('baidu', service.Baidu),
            ('collins', service.Collins),
            ('duden', service.Duden),
            ('ekho', service.Ekho),
            ('espeak', service.ESpeak),
            ('festival', service.Festival),
            ('fluencynl', service.FluencyNl),
            ('google', service.Google),
            ('howjsay', service.Howjsay),
            ('imtranslator', service.ImTranslator),
            ('ispeech', service.ISpeech),
            ('naver', service.Naver),
            ('neospeech', service.NeoSpeech),
            ('oddcast', service.Oddcast),
            ('oxford', service.Oxford),
            ('pico2wave', service.Pico2Wave),
            ('rhvoice', service.RHVoice),
            ('sapi5com', service.SAPI5COM),
            ('sapi5js', service.SAPI5JS),
            ('say', service.Say),
            ('spanishdict', service.SpanishDict),
            ('voicetext', service.VoiceText),
            ('wiktionary', service.Wiktionary),
            ('yandex', service.Yandex),
            ('youdao', service.Youdao),
        ],
        dead=dict(
            ttsapicom="TTS-API.com has gone offline and can no longer be "
                      "used. Please switch to another service with English.",
        ),
        aliases=[('b', 'baidu'), ('g', 'google'), ('macosx', 'say'),
                 ('microsoft', 'sapi5js'), ('microsoftjs', 'sapi5js'),
                 ('microsoftjscript', 'sapi5js'), ('oed', 'oxford'),
                 ('osx', 'say'), ('sapi', 'sapi5js'), ('sapi5', 'sapi5js'),
                 ('sapi5jscript', 'sapi5js'), ('sapijs', 'sapi5js'),
                 ('sapijscript', 'sapi5js'), ('svox', 'pico2wave'),
                 ('svoxpico', 'pico2wave'), ('ttsapi', 'ttsapicom'),
                 ('windows', 'sapi5js'), ('windowsjs', 'sapi5js'),
                 ('windowsjscript', 'sapi5js'), ('y', 'yandex')],
        normalize=to.normalized_ascii,
        args=(),
        kwargs=dict(temp_dir=paths.TEMP,
                    lame_flags=lambda: config['lame_flags'],
                    normalize=to.normalized_ascii,
                    logger=logger,
                    ecosystem=Bundle(web=WEB, agent=AGENT)),
    ),
    cache_dir=paths.CACHE,
    temp_dir=join(paths.TEMP, '_awesometts_scratch_' + str(int(time()))),
    logger=logger,
    config=config,
)
