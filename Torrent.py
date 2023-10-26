import utils.BEncode as Encoder
import utils.BDecode as Decoder
from urllib.parse import quote
from utils import Metadata
import hashlib
import random
import requests

class Torrent:

    def __init__(self, torrent_file, port):
        self.encoder = Encoder.BEncode()
        self.decoder = Decoder.BDecode()
        self.torrent_file = torrent_file
        self.port = port

    def get_metadata(self):
        bytes_metadata = self.decoder.decode(self.torrent_file.read())
        self.metadata = Metadata.Metadata().bytes_to_str(bytes_metadata)

    def info_hash(self):
        return quote(hashlib.sha1(self.encoder.encode(self.metadata['info'])).digest(), safe='')
    
    def generate_id(self):
        return f'-MM0001-{''.join([str(random.randint(0, 9)) for i in range(12)])}'
    
    def get_tracker_request(self):
        self.get_metadata()
        url = f'{self.metadata['announce']}?'
        url += f'info_hash={self.info_hash()}&'
        url += f'peer_id={quote(self.generate_id())}&'
        url += f'port={self.port}&'
        url += f'uploaded=0&'
        url += f'downloaded=0&'
        url += f'left={self.metadata['info']['length']}&'
        url += f'compact=1'
        return url
    
with open('torrents//ubuntu-23.10.1-desktop-amd64.iso.torrent', 'rb') as f:
    test = Torrent(f, 6889)
    url = test.get_tracker_request()
    print(url)
    response = requests.get(url)
    content = response.content
    test_decode = Decoder.BDecode()
    print(response, test_decode.decode(content, current_index=[0]))
    #print(quote(test.info_hash().digest(), safe=''))