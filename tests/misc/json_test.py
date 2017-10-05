from tests.misc.packet import *

TOTAL_DEFS = 3

URL_WORDS = "https://crunchprep.com/gre/2014/101-high-frequency-gre-words"
URL_GSTA = "http://ssl.gstatic.com/dictionary/static/sounds/oxford/"
URL_DICT = "http://dictionary.reference.com/browse/"
GB_1 = "--_gb_1.mp3"        # A trailing type for gstatic dictionary
GB_18 = "--_gb_1.8.mp3"     # A trailing type for gstatic dictionary

TEMP_DIR = "./TEMPLATE/"
TEST_DIR = "./test_mp3/"
MERG_DIR = "./MERGED/"
MP3 = ".mp3"


r = requests.get(URL_WORDS)
data = r.text

soup = BeautifulSoup(data, "html.parser")
words = soup.find_all("strong")
words = [word.text.lower() for word in words[1:102]]

for n, word in enumerate(words[0:50]):
    p = Packet(word, n+1)
    p.getJsonForm()


