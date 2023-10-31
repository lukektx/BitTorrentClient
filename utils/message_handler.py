from . import message_decoder as decoder

class MessageHandler:
    def __init__ (self, peer):
        self.peer = peer
        self.HANDLER_ACTIONS = {
            decoder.MessageType.KEEP_ALIVE: self.keep_alive,
            decoder.MessageType.CHOKE: self.choke,
            decoder.MessageType.UNCHOKE: self.unchoke,
            decoder.MessageType.INTERESTED: self.interested,
            decoder.MessageType.NOT_INTERESTED: self.not_interested,
            decoder.MessageType.HAVE: self.have,
            decoder.MessageType.BITFIELD: self.bitfield,
            decoder.MessageType.REQUEST: self.request,
            decoder.MessageType.PIECE: self.piece,
            decoder.MessageType.CANCEL: self.cancel,
            decoder.MessageType.PORT: self.port,
        }

    def keep_alive(self):
        self.peer.update_time()
    def choke(self):
        self.peer.choke()
    def unchoke(self):
        self.peer.unchoke()
    def interested(self):
        self.peer.interested()
    def not_interested(self):
        self.peer.not_interested()
    def have(self, message):
        self.peer.update_bitfield_index(message['piece_index'])
    def bitfield(self, message):
        self.peer.set_bitfield(message['bitfield'])
    def request(self, message):
        self.peer.send_block(message['index'], message['begin'], message['length'])
    def piece(self, message):
        self.peer.add_block(message['index'], message['begin'], message['block'])
    def cancel(self, message):
        self.peer.cancel(message['index'], message['begin'], message['length'])
    def port(self, message):
        self.peer.port(message['port'])

    def handle_message(self, message):
        if not self.peer.get_handshake_status():
            if message: # TODO check if message is a handshake
                self.peer.handshake()
            else:
                self.peer.set_connection_status(False)
        else:
            self.upload_handler(message)

    def download_handler(self, message):
        if (
            self.peer.status.choked() and
            message['id'] != decoder.MessageType.UNCHOKE and
            message['id'] != decoder.MessageType.BITFIELD
        ):
            pass
            

    def upload_handler(self, message):
        if (
            self.peer.status.get_choke_status() and
            message['id'] != decoder.MessageType.UNCHOKE and
            message['id'] != decoder.MessageType.BITFIELD
        ):
            print('recieved invalid message (peer still choked)')
            self.peer.set_connection_status(False)
            return
        else:
            print('message:', message)
            self.HANDLER_ACTIONS[message['id']](message)