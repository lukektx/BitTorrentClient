class Messages:

    def __init__(self, info_hash, peer_id):
        self.PSTR = b'BitTorrent protocol'
        self.info_hash = info_hash
        self.peer_id = peer_id

    def handshake(self, info_hash, peer_id):
        pstrlen = len(self.PSTR).to_bytes(1, 'big')
        reserved = b'\x00' * 8
        return pstrlen + self.PSTR + reserved + self.info_hash + self.peer_id
    def keep_alive():
        length = b'\x00' * 4
        return length
    def choke():
        length = b'\x00' * 3 + b'\x01'
        id = b'\x00'
        return length + id
    def unchoke():
        length = b'\x00' * 3 + b'\x01'
        id = b'\x01'
        return length + id
    def interested():
        length = b'\x00' * 3 + b'\x01'
        id = b'\x02'
        return length + id
    def not_interested():
        length = b'\x00' * 3 + b'\x01'
        id = b'\x03'
        return length + id
    def have(piece_index):
        length = b'\x00' * 3 + b'\x01'
        id = b'\x03'
        return length + id
        return 
    def bitfield():
        pass
    def request():
        pass
    def piece():
        pass
    def cancel():
        pass
    def port():
        pass