from utils import connections
from utils import message_handler
from utils import messages
import peer_status

class Peer:

    def __init__(self, torrent, connection, ip, port):
        if connection:
            self.connection = connections.PeerConnection(connection, ip, port)
        else:
            self.connection = connections.PeerDownload(ip, port)
            self.connection.socket_connect()

        self.status = peer_status.PeerStatus()
        self.handler = message_handler.MessageHandler(self)
        self.torrent = torrent
        self.bitfield = b''

    def __str__(self):
        return f'Peer connection = {self.connection.ip}:{self.connection.port}'

    # TODO check if peer times out

    def get_connection_status(self):
        return self.status.connection_status

    def await_handshake(self):
        message = self.connection.recieve_handshake()
        if not message:
            self.status.set_connection_status(False)
            return
        if not self.torrent.info_hash() == message['info_hash']:
            print('Handshake had different hash')
            self.status.set_connection_status(False)
            return
        self.status.set_handshake_status(True)
        return message


    def download_piece(self, index, offset, length):
        # TODO handshake if needed, send interested, get unchoked, then request
        data = b''
        self.torrent.add_piece(index, offset, data)

    def handle_message(self):
        message = self.connection.recieve_message()
        self.handler.handle_message(message)

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

    def get_choke_status(self):
        return self.status.get_choke_status()

    def get_interested_status(self):
        return self.status.get_interested_status()
    
    def get_handshake_status(self):
        return self.status.get_handshake_status()
    
    def get_connection_status(self):
        return self.status.get_connection_status()

    def update_bitfield_index(self, piece_index):
        self.bitfield.set_piece_status(piece_index)

    def set_bitfield(self, bitfield):
        self.bitfield = bitfield

    def get_bitfield(self):
        return self.bitfield

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