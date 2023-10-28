import message_decoder as decoder
import messages

class MessageHandler:
    def __init__ (self, peer):
        self.peer = peer

    def keep_alive(self, message):
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

    HANDLER_ACTIONS = {
        decoder.MessageType.KEEP_ALIVE: keep_alive,
        decoder.MessageType.CHOKE: choke, 
        decoder.MessageType.UNCHOKE: unchoke,
        decoder.MessageType.INTERESTED: interested,
        decoder.MessageType.NOT_INTERESTED: not_interested,
        decoder.MessageType.HAVE: have,
        decoder.MessageType.BITFIELD: bitfield,
        decoder.MessageType.REQUEST: request,
        decoder.MessageType.PIECE: piece,
        decoder.MessageType.CANCEL: cancel,
        decoder.MessageType.PORT: port
    }

    def handle_message(self, message):
        self.HANDLER_ACTIONS[message['id']](message)
