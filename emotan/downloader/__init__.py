from emotan.downloader.dictionarycom import DictionaryComDownloader
from emotan.downloader.cambridge import CambridgeDownloader
from emotan.downloader.oxford import OxfordDownloader
from emotan.downloader.wiktionary import WiktionaryDownloader

Downloaders = {
    "Dictionary.com": DictionaryComDownloader,
    "Cambridge Dictionary": CambridgeDownloader,
    "Oxford English Dictionary": OxfordDownloader,
    "Wiktionary": WiktionaryDownloader
}
