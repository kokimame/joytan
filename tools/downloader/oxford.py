from tools.downloader.base import BaseDownloader

class OxfordDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__(self)
        self.sourceUrl = "https://en.oxforddictionaries.com/definition/"
        self.sourceName = "Oxford English Dictionary"