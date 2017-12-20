class BaseDownloader:
    def __init__(self):
        # Each Downloader class prefers to be instantiated only once
        # in a downloading session. This leads to make Downloader to be initialized
        # without HTML data to donwload from. Every HTML will be passed in run method.

        # Every downloader has its own source. e.g, Online dictionaries
        self.source_url = None
        self.source_name = None

    def run(self, data):
        """
        # :param: data - HTML data to download from
        # :return: Contents related with an Entry, such as 'definition' and 'image'
        # Each class implements a run method specific to their source.
        # Download only once for an entry even if 
        # Entry preference modified after the downloading session.
        #
        # FIXME: Child classes are using ugly way of passing downloded contents to each entry.
        # Save all downloaded contents tagging with lineKey and overwrite entry's editors.
        """
        raise NotImplementedError