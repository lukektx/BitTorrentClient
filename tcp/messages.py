def message(id=0, payload=b''):
    if not id:
        return int(0).to_bytes(4, 'big')
    return (len(str(id)) + len(payload)).to_bytes(4, 'big') + id.to_bytes(1, 'big') + payload

def handshake(info_hash, peer_id):
    PSTR = b'BitTorrent protocol'
    pstrlen = len(PSTR).to_bytes(4, 'big')
    reserved = b'\x00' * 8
    return pstrlen + PSTR + reserved + info_hash + peer_id

def keep_alive():
    return message(None)

def choke():
    return message(0)

def unchoke():
    return message(1)

def interested():
    return message(2)

def not_interested():
    return message(3)

def have(piece_index):
    return message(4, piece_index.to_bytes(4, 'big'))

def bitfield(bitfield):
    return message(5, bitfield.to_bytes(4, 'big'))

def request(index, offset, length):
    payload = index.to_bytes(4, 'big') + offset.to_bytes(4, 'big') + length.to_bytes(4, 'big')
    return message(6, payload)

def piece(index, offset, block):
    payload = index.to_bytes(4, 'big') + offset.to_bytes(4, 'big') + block.to_bytes(4, 'big')
    return message(7, payload)

def cancel(index, offset, length):
    payload = index.to_bytes(4, 'big') + offset.to_bytes(4, 'big') + length.to_bytes(4, 'big')
    return message(8, payload)

def port(port):
    return message(9, port.to_bytes(2, 'big'))