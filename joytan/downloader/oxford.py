from joytan.downloader.base import BaseDownloader

class OxfordDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__(self)
        self.source_url = "https://en.oxforddictionaries.com/definition/"
        self.source_name = "Oxford English Dictionary"