from .base import Service
from .common import Trait

import boto3
from contextlib import closing

__all__ = ['Amazon']

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

        return [
            dict(
                key='voice',
                label="Voice",
                values=self._voice_list,
                transform=transform_voice,
            )
        ]

    def run(self, text, options, path):
        """
        Writes mp3 file directly 
        """
        output_file = path

        try:
            r = self.polly.synthesize_speech(VoiceId=options['voice'],
                                             Text=text,
                                             OutputFormat='mp3')

            with closing(r['AudioStream']) as stream:
                with open(output_file, 'wb') as f:
                    f.write(stream.read())

        except Exception as e:
            raise Exception("Amazon Polly returned Exception %s" % e)


