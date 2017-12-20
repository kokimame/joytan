from emotan.downloader.base import BaseDownloader

class CambridgeDownloader(BaseDownloader):
    def __init__(self):
        BaseDownloader.__init__()
        self.source_url = "http://dictionary.cambridge.org/dictionary/english/"
        self.source_name = "Cambridge Dictionary"