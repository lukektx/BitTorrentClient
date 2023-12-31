import utils.BEncode as Encoder
import utils.BDecode as Decoder
from urllib.parse import quote
from utils import messages
from utils import connections
import peer
import torrent_statistics
import download_queue
import piece_tracker
import file_handler
import TrackerResponse
import hashlib
import random
import requests
import threading
import time

HASH_SIZE = 20
RANDOM_DOWNLOADS = 4

class Torrent:

    def __init__(self, torrent_file, path, port, max_peers, operation):
        self.encoder = Encoder.BEncode()
        self.decoder = Decoder.BDecode()
        self.torrent_file = torrent_file
        self.metadata = self.read_torrent(torrent_file)
        self.pieces = piece_tracker.PieceTracker(
            file_handler.FileHandler(f'{path}//{self.metadata['info']['name']}'),
            self.metadata['info']['pieces'],
            self.metadata['info']['piece length'], 
            len(self.metadata['info']['pieces']) // HASH_SIZE
        )
        if operation == 'seed':
            #check the pieces we have downloaded to be sure hashes match
            self.set_valid_pieces()
        self.download_queue = download_queue.DownloadQueue()
        self.statistics = torrent_statistics.TorrentStatistics()
        self.max_peers = max_peers
        self.peers = []
        self.port = port
        self.id = bytes(self.generate_id(), 'utf-8')
        self.block_size = 2 ** 14 #16kb (standard request size)

    # TODO Implement torrent statistics (upload/download/ratio/etc)

    def read_torrent(self, torrent_file):
        with open(torrent_file, 'rb') as f:
            metadata = f.read()
            decoded = self.decoder.decode(metadata)
            return decoded
        
    def set_valid_pieces(self):
        print('confirming piece hashes')
        for index in range(len(self.metadata['info']['pieces']) // HASH_SIZE):
            if(self.pieces.check_hash(index, disk=True)):
                self.pieces.set_bitfield_status(index)

        print('valid pieces:', self.pieces.num_downloaded_pieces())
        print('total pieces:', len(self.metadata['info']['pieces']) // HASH_SIZE)

    def info_hash(self):
        return hashlib.sha1(self.encoder.encode(self.metadata['info'])).digest()
    
    def generate_id(self):
        return f'-MM0001-{''.join([str(random.randint(0, 9)) for i in range(12)])}'
    
    def get_tracker_request(self):
        url = f'{self.metadata['announce']}?'
        url += f'info_hash={quote(self.info_hash(), safe='')}&'
        url += f'peer_id={quote(self.id)}&'
        url += f'port={self.port}&'
        url += f'uploaded=0&'
        url += f'downloaded=0&'
        url += f'left={self.metadata['info']['length']}&'
        url += f'compact=1'
        return url

    def get_block(self, index, begin, length):
        return self.pieces.get_block(index, begin, length)
        
    def add_block(self, index, begin, block):
        return self.pieces.set_block(index, begin, block)

    def find_peers(self):
        # TODO request peer info from the tracker
        TEST_PEER_ADDRESS = ['localhost', 6889]
        self.peers.append(peer.Peer(self, None, TEST_PEER_ADDRESS[0], TEST_PEER_ADDRESS[1]))
            
    def connect_peers(self):
        for peer in self.peers:
            peer.connect()
            peer.send_handshake()
            response = peer.await_handshake()
            print(f'recieved handshake {response}')
    
    def download(self):
        self.set_download_order()
        for peer in self.peers:
            threading.Thread(target=self.download_piece, args=(peer,)).start()

    def set_download_order(self):
        self.select_download_algo()

    def select_download_algo(self):
        if self.pieces.num_downloaded_pieces() < 4:
            self.random_first()
        elif self.pieces.num_downloaded_pieces() >= 4:
            self.rarest_first()
        # TODO add endgame download rules

    def random_first(self):
        needed = self.pieces.remaining_pieces()
        print('need', needed)
        chosen = []
        for i in range(min(RANDOM_DOWNLOADS, len(needed))):
            chosen.append(needed[random.randint(0, len(needed) - 1)])
        self.download_queue.enable_strict_priority()
        self.download_queue.set_queue(chosen)

    def get_bitfield(self):
        return self.pieces.get_bitfield()

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
        print('need piece', piece)
        sent_requests = 0
        if not piece:
            print('no pieces needed from peer')
            return

        while piece:
            if sent_requests < 25:
                try:
                    finished = peer.download_piece(piece)
                except ValueError:
                    print('Failed piece download, hash doesn\'t match')
                    self.pieces.reset_piece(piece)
                if finished:
                    piece = self.download_queue.get_needed_piece()
                    self.download_queue.remove_piece(piece)
            else:
                time.sleep(1)

    def add_piece(self, index, begin, block):
        self.pieces.set_block(index, begin, block)

    def begin_seeding(self):
        HOST, PORT = '', self.port
        self.peer_finder = connections.OwnConnection(self.max_peers, HOST, PORT)
        self.peer_finder.socket_connect()
        seeding = True
        while seeding:
            new_connection = self.peer_finder.acquire_connection()
            if new_connection:
                conn, addr = new_connection
                ip, port = addr
                new_peer = peer.Peer(self, conn, ip, port)
                self.peers.append(new_peer)
                print('starting thread')
                threading.Thread(target=self.start_listening, args=(new_peer,)).start()

    
    @staticmethod
    def start_listening(peer):
        print('started listening to', peer)
        peer_info = peer.await_handshake()
        peer.send_handshake()
        peer.send_bitfield()

        print('got handshake info', peer_info)
        while peer.get_connection_status():
            peer.handle_message()
        print('closing peer thread', peer)
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
