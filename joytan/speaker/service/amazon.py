# -*- coding: utf-8 -*-
# Copyright (C) 2017-Present: Koki Mametani <kokimametani@gmail.com>
# License: GNU version 3 or later; http://www.gnu.org/licenses/gpl.html

from .base import Service
from .common import Trait

import boto3
from contextlib import closing

__all__ = ['Amazon']

# Speech Synthesis Markup Language (SSML)
# This format specifies the timbre of speech of Amazon Polly and
# will be passed to the service after user configuring properties at ATTS GUI.
# Now we only edit the speed (rate) with this format in addition to the voice,
# which is determined separately.
# The other supported properties such as pitch and volume need another combobox
# in ATTS GUI, but originally the GUI has only 2 combobox (voice and variant),
# which are already taken, with some spinbox.
# But because Amazon Polly controls properties by categories not by integer nor float,
# we have to have more combobox in the GUI.
SSML = """
<speak>
<prosody rate="{rate}">
{text}
</prosody>
</speak>
"""

class Amazon(Service):
    """
    Provides a Service-compliant implementation for Amazon Polly
    See the API of Boto3 for Polly:
    -> https://boto3.readthedocs.io/en/latest/reference/services/polly.html
    """

    NAME = "Amazon Polly"

    TRAITS = []

    def __init__(self, *args, **kwargs):
        super(Amazon, self).__init__(*args, **kwargs)

        # TODO: Look for AWS credentials and validate availability of this service.
        # try:
        #       validate
        # except:
        #       showCritical("Guiding how to activate Polly")
        #       return ?

        self.polly = boto3.client('polly')

        self._voice_list = [
            (item['Name'], "%s (%s)" % (item['Name'], item['LanguageName']))
            for item in sorted(
                self.polly.describe_voices()['Voices'], key=lambda x: x['LanguageCode'])
        ]

        if not self._voice_list:
            raise EnvironmentError("No usable voice from Amazon Polly. "
                                   "This must be a server-side error")

    def desc(self):
        """
        Returns a short, static description 
        """
        return "%s (%d voices)" % (
            "Amazon Polly: AWS product",
            len(self.polly.describe_voices()['Voices']),
        )

    def options(self):
        """
        Provides access to voice         
        """

        voice_lookup = {
            self.normalize(voice[0]) : voice[0]
            for voice in self._voice_list
        }

        def transform_voice(value):
            """Normalize and attempt to convert to official voice."""

            normalized = self.normalize(value)

            return (
                voice_lookup[normalized] if normalized in voice_lookup
                else value
            )
# x-slow, slow, medium, fast, x-fast
        return [
            dict(
                key='voice',
                label="Voice",
                values=self._voice_list,
                transform=transform_voice,
            ),
            dict(
                key='variant',
                label="Speed",
                values=[
                    (speed, speed) for speed in
                    ['x-slow', 'slow', 'medium', 'fast', 'x-fast']
                ],
                transform=lambda x: x,
                default="medium"
            )
        ]

    def run(self, text, options, path):
        """
        Writes mp3 file directly 
        """
        output_file = path

        text = SSML.format(text=text,
                           rate=options['variant'])

        try:
            r = self.polly.synthesize_speech(VoiceId=options['voice'],
                                             Text=text,
                                             TextType='ssml',
                                             OutputFormat='mp3')

            with closing(r['AudioStream']) as stream:
                with open(output_file, 'wb') as f:
                    f.write(stream.read())

        except Exception as e:
            raise Exception("Amazon Polly returned Exception %s" % e)


