from enum import Enum

class MessageType(Enum):
    KEEP_ALIVE = None
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7
    CANCEL = 8
    PORT = 9

INT_PARAM_BYTES = 4 #length of integer data passed such as an index or offset in a request
LENGTH_BYTES = 4
ID_BYTES = 1

def extract_data(raw_data):
    length = int.from_bytes(raw_data[0:LENGTH_BYTES], "big")
    if(len(raw_data) - LENGTH_BYTES != length):
        #TODO handle invalid transmission (length != expected_len)
        return
    try:
        id = int.from_bytes(raw_data[LENGTH_BYTES:LENGTH_BYTES+ID_BYTES], "big")
        payload = raw_data[LENGTH_BYTES+ID_BYTES:LENGTH_BYTES+length]
    except IndexError:
        #no id (keep alive message)
        id = None
        payload = b''
    
    return {'length': length, 'id': id, 'payload': payload}

def extract_payload(parsed_data):
    #delete key payload to assign to new name specific to message type
    payload = parsed_data['payload']
    del parsed_data['payload']

    match parsed_data['id']:
        case MessageType.HAVE:
            parsed_data['piece_index'] = payload
        
        case MessageType.BITFIELD:
            parsed_data['bitfield'] = payload

        case MessageType.REQUEST:
            parsed_data['index'] = payload[LENGTH_BYTES+ID_BYTES: LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES]
            parsed_data['begin'] = payload[LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES: LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES]
            parsed_data['length'] = payload[LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES:]

        case MessageType.PIECE:
            parsed_data['index'] = payload[LENGTH_BYTES+ID_BYTES: LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES]
            parsed_data['begin'] = payload[LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES: LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES]
            parsed_data['block'] = payload[LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES:]

        case MessageType.CANCEL:
            parsed_data['index'] = payload[LENGTH_BYTES+ID_BYTES: LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES]
            parsed_data['begin'] = payload[LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES: LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES]
            parsed_data['length'] = payload[LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES:]

        case MessageType.PORT:
            parsed_data['listen_port'] = payload

    return parsed_data
    