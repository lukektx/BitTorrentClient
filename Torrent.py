import utils.BEncode as Encoder
import utils.BDecode as Decoder
from urllib.parse import quote
from utils import ByteDecoder
from utils import messages
import PieceTracker
import TrackerResponse
import hashlib
import random
import requests

class Torrent:

    def __init__(self, torrent_file, port):
        self.encoder = Encoder.BEncode()
        self.decoder = Decoder.BDecode()
        self.torrent_file = torrent_file
        self.metadata = self.decoder.decode(self.torrent_file.read())
        print(self.metadata)
        self.pieces = PieceTracker.PieceTracker(self.metadata[''])
        self.port = port
        self.block_size = 16384

    def info_hash(self):
        return quote(hashlib.sha1(self.encoder.encode(self.metadata['info'])).digest(), safe='')
    
    def generate_id(self):
        return f'-MM0001-{''.join([str(random.randint(0, 9)) for i in range(12)])}'
    
    def get_tracker_request(self):
        url = f'{self.metadata['announce']}?'
        url += f'info_hash={self.info_hash()}&'
        url += f'peer_id={quote(self.generate_id())}&'
        url += f'port={self.port}&'
        url += f'uploaded=0&'
        url += f'downloaded=0&'
        url += f'left={self.metadata['info']['length']}&'
        url += f'compact=1'
        return url
    
if __name__ == '__main__':
    with open('torrents//ubuntu-23.10.1-desktop-amd64.iso.torrent', 'rb') as f:
        test = Torrent(f, 6889)
        url = test.get_tracker_request()
        print(url)
        print(test.metadata)
        print(messages.have(27))
        print(messages.request(0,0,test.block_size))

        # response = requests.get(url)
        # content = response.content
        
        # test_resp = TrackerResponse.TrackerResponse(content)
        # print(test_resp.get_peers())