from tools.downloader.dictionarycom import DictionaryComDownloader
from tools.downloader.cambridge import CambridgeDownloader
from tools.downloader.oxford import OxfordDownloader
from tools.downloader.wiktionary import WiktionaryDownloader

Downloaders = {
    "Dictionary.com": DictionaryComDownloader,
    "Cambridge Dictionary": CambridgeDownloader,
    "Oxford English Dictionary": OxfordDownloader,
    "Wiktionary": WiktionaryDownloader
}
