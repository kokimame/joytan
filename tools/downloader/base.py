class BaseDownloader:
    def __init__(self):
        # Each Downloader class prefers to be instantiated only once
        # in a downloading session. This leads to make Downloader to be initialized
        # without HTML data to donwload from. Every HTML will be passed in run method.

        # Every downloader has its own source. e.g, Online dictionaries
        self.sourceUrl = None
        self.sourceName = None

    def run(self, data):
        """
        :param: data - HTML data to download from
        :return: Contents related with an Entry, such as 'definition' and 'image'
        All Downloader classes need to overwrite this method.
        Download and return contents as much as possible.
        Download only once for an entry even if Entry preference modified
        after the downloading session.
        Each class uses a run method specific to their target dictionary.
        """
        raise NotImplementedError