import utils.BEncode as Encoder
import utils.BDecode as Decoder
from urllib.parse import quote
from utils import messages
from utils import connections
import peer
import download_queue
import piece_tracker
import TrackerResponse
import hashlib
import random
import requests
import threading
from enum import Enum

HASH_SIZE = 20
RANDOM_DOWNLOADS = 4

class Torrent:

    def __init__(self, torrent_file, out_path, port, max_peers, operation):
        self.encoder = Encoder.BEncode()
        self.decoder = Decoder.BDecode()
        self.torrent_file = torrent_file
        self.metadata = self.decoder.decode(self.torrent_file.read())
        if operation == 'download':
            self.pieces = piece_tracker.PieceTracker(
                self.metadata['pieces'], 
                self.metadata['pieces length'], 
                len(self.metadata['pieces']) / HASH_SIZE
            )
        self.peers = []
        self.port = port
        self.block_size = 2 ** 14 #16kb (standard request size)
        self.download_queue = download_queue.DownloadQueue()

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
    
    def get_block(self, index, begin, length):
        return self.pieces.get_piece(index, begin, length)
        
    def add_block(self, index, begin, block):
        return self.pieces.set_piece(index, begin, block)

    def find_peers(self):
        # TODO request peer info from the tracker
        peers = []
        pass

    def connect_peers(self):
        for peer in self.peers:
            peer.setup_peer()
            peer.handshake()
            
    def download(self):
        self.set_download_order()
        for peer in self.peers:
            threading.Thread(target=self.download_piece, args=(peer,))

    def set_download_order(self):
        self.select_download_algo()

    def select_download_algo(self, algorithm):
        if self.pieces.num_downloaded_pieces() < 4:
            self.random_first()
        elif self.pieces.num_downloaded_pieces() >= 4:
            self.rarest_first()
        # TODO add endgame download rules

    def random_first(self):
        needed = self.pieces.remaining_pieces()
        chosen = []
        for i in range(RANDOM_DOWNLOADS):
            chosen.append(needed[random.randint(0, len(needed) - 1)])
        self.download_queue.enable_strict_priority()
        self.download_queue.set_queue(chosen)

    def get_rarities(self):
        bitfields = [peer.get_bitfield() for peer in self.peers]
        return [sum([bitfields[j][i] for j in range(len(bitfields))]) for i in range(len(bitfields[0]))]

    def rarest_first(self):
        rarities = [(index, rarity) for index, rarity in enumerate(self.get_rarities())]
        rarities.sort(key=lambda e: e[1] if e[1] > 0 else float('infinity'))
        self.download_queue.disable_strict_priority()
        self.download_queue.set_queue([rarities[i][0] for i in range(len(rarities))])

    def download_piece(self, peer):
        piece = self.download_queue.get_needed_piece()
        finished = False
        try:
            finished = peer.download_piece(piece)
        except ValueError:
            print('Failed piece download, hash doesn\'t match')
            self.pieces.reset_piece(piece)
        if finished:
            self.download_queue.remove_piece(piece)


    def add_piece(self, index, begin, block):
        self.pieces.set_piece(index)


    def begin_seeding(self):
        
        HOST, PORT = '', self.port
        self.peer_finder = connections.OwnConnection(1, HOST, PORT)
        self.peer_finder.socket_connect()
        seeding = True
        while seeding:
            new_connection = self.peer_finder.acquire_connection()
            if new_connection:
                conn, addr = new_connection
                ip, port = addr
                new_peer = peer.Peer(self, conn, ip, port)
                self.peers.append(new_peer)
                threading.Thread(target=self.start_listening, args=(peer,))
    
    def start_listening(peer):
        while peer.connection and peer.status.get_interested_status():
            peer.handle_message()
        peer.connection.peer_socket.close()

    
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