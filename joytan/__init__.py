import os
import sys

from . import conversion as to
from .bundle import Bundle
from .config import Config

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


CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.db')

# Begin core class initialization and dependency setup, pylint:disable=C0103

logger = Bundle(debug=lambda *a, **k: None, error=lambda *a, **k: None,
                info=lambda *a, **k: None, warn=lambda *a, **k: None)
# for logging output, replace `logger` with a real one, e.g.:
# import logging as logger
# logger.basicConfig(stream=sys.stdout, level=logger.DEBUG)

config = Config(
    db=Bundle(path=CONFIG,
              table='general',
              normalize=to.normalized_ascii),
    cols=[
        # ('automaticAnswers', 'integer', True, to.lax_bool, int),
        # ('automatic_answers_errors', 'integer', True, to.lax_bool, int),
        # ('automaticQuestions', 'integer', True, to.lax_bool, int),
        # ('automatic_questions_errors', 'integer', True, to.lax_bool, int),
        # ('cache_days', 'integer', 365, int, int),
        # ('delay_answers_onthefly', 'integer', 0, int, int),
        # ('delay_answers_stored_ours', 'integer', 0, int, int),
        # ('delay_answers_stored_theirs', 'integer', 0, int, int),
        # ('delay_questions_onthefly', 'integer', 0, int, int),
        # ('delay_questions_stored_ours', 'integer', 0, int, int),
        # ('delay_questions_stored_theirs', 'integer', 0, int, int),
        # ('ellip_note_newlines', 'integer', False, to.lax_bool, int),
        # ('ellip_template_newlines', 'integer', False, to.lax_bool, int),
        ('extras', 'text', {}, to.deserialized_dict, to.compact_json),
        ('filenames', 'text', 'hash', str, str),
        ('filenames_human', 'text',
         '{{text}} ({{service}} {{voice}})', str, str),
        ('groups', 'text', {}, to.deserialized_dict, to.compact_json),
        ('lame_flags', 'text', '--quiet -q 2', str, str),
        # ('last_mass_append', 'integer', True, to.lax_bool, int),
        # ('last_mass_behavior', 'integer', True, to.lax_bool, int),
        # ('last_mass_dest', 'text', 'Back', str, str),
        # ('last_mass_source', 'text', 'Front', str, str),
        ('last_options', 'text', {}, to.deserialized_dict, to.compact_json),
        ('last_service', 'text', ('sapi5js' if 'win32' in sys.platform
                                  else 'say' if 'darwin' in sys.platform
                                  else 'espeak'), str, str),
        # ('last_strip_mode', 'text', 'ours', str, str),
        # ('launch_browser_generator', 'integer', Qt.ControlModifier | Qt.Key_T,
        #  to.nullable_key, to.nullable_int),
        # ('launch_browser_stripper', 'integer', None, to.nullable_key,
        #  to.nullable_int),
        # ('launch_configurator', 'integer', Qt.ControlModifier | Qt.Key_T,
        #  to.nullable_key, to.nullable_int),
        # ('launch_editor_generator', 'integer', Qt.ControlModifier | Qt.Key_T,
        #  to.nullable_key, to.nullable_int),
        # ('launch_templater', 'integer', Qt.ControlModifier | Qt.Key_T,
        #  to.nullable_key, to.nullable_int),
        # ('otf_only_revealed_cloze', 'integer', False, to.lax_bool, int),
        # ('otf_remove_hints', 'integer', False, to.lax_bool, int),
        ('presets', 'text', {}, to.deserialized_dict, to.compact_json),
        # ('spec_note_count', 'text', '', str, str),
        # ('spec_note_count_wrap', 'integer', True, to.lax_bool, int),
        # ('spec_note_ellipsize', 'text', '', str, str),
        # ('spec_note_strip', 'text', '', str, str),
        # ('spec_template_count', 'text', '', str, str),
        # ('spec_template_count_wrap', 'integer', True, to.lax_bool, int),
        # ('spec_template_ellipsize', 'text', '', str, str),
        # ('spec_template_strip', 'text', '', str, str),
        # ('strip_note_braces', 'integer', False, to.lax_bool, int),
        # ('strip_note_brackets', 'integer', False, to.lax_bool, int),
        # ('strip_note_parens', 'integer', False, to.lax_bool, int),
        # ('strip_template_braces', 'integer', False, to.lax_bool, int),
        # ('strip_template_brackets', 'integer', False, to.lax_bool, int),
        # ('strip_template_parens', 'integer', False, to.lax_bool, int),
        # ('sub_note_cloze', 'text', 'anki', str, str),
        # ('sub_template_cloze', 'text', 'anki', str, str),
        # ('sul_note', 'text', [], to.substitution_list, to.substitution_json),
        # ('sul_template', 'text', [], to.substitution_list,
        #  to.substitution_json),
        # ('templater_cloze', 'integer', True, to.lax_bool, int),
        # ('templater_field', 'text', 'Front', str, str),
        # ('templater_hide', 'text', 'normal', str, str),
        # ('templater_target', 'text', 'front', str, str),
        # ('throttle_sleep', 'integer', 30, int, int),
        # ('throttle_threshold', 'integer', 10, int, int),
        # ('TTS_KEY_A', 'integer', Qt.Key_F4, to.nullable_key, to.nullable_int),
        # ('TTS_KEY_Q', 'integer', Qt.Key_F3, to.nullable_key, to.nullable_int),
        # ('updates_enabled', 'integer', True, to.lax_bool, int),
        # ('updates_ignore', 'text', '', str, str),
        # ('updates_postpone', 'integer', 0, int, lambda i: int(round(i))),
    ],
    logger=logger,
    events=[
    ],
)
