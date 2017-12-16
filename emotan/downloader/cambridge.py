from emotan.downloader.base import BaseDownloader

class CambridgeDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__()
        self.sourceUrl = "http://dictionary.cambridge.org/dictionary/english/"
        self.sourceName = "Cambridge Dictionary"