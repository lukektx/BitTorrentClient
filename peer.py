from tcp import connections
from utils import message_handler
from utils import messages
import peer_status
import piece_tracker

class Peer:

    def __init__(self, torrent, connection, ip, port):
        self.connecion = connections.PeerConnection(connection, ip, port)
        self.status = peer_status.PeerStatus()
        self.handler = message_handler.MessageHandler(self)
        self.bitfield = b''

    def update_time(self):
        self.status.update_time()

    def choke(self):
        self.status.choke()

    def unchoke(self):
        self.status.unchoke()

    def interested(self):
        self.status.interested()

    def not_interested(self):
        self.status.not_interested()

    def update_bitfield_index(self, piece_index):
        self.bitfield.set_piece_status(piece_index)

    def set_bitfield(self, bitfield):
        self.bitfield = bitfield

    def send_block(self, index, begin, length):
        block = self.torrent.get_block(index, begin, length)
        self.connection.send_data(messages.piece(index, begin, block))

    def add_block(self, index, begin, block):
        completed = self.torrent.add_block(index, begin, block)
        # TODO if piece completed, send a have to announce we have this piece now

    def cancel(index, begin, length):
        # TODO dont send piece if we havent already
        pass

    def port(port):
        # TODO read more about this and DHT tracker then implement 
        pass