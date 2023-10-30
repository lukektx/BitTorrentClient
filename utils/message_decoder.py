from enum import IntEnum
from . import byte_decoder

class MessageType(IntEnum):
    KEEP_ALIVE = -1
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

def extract_payload(parsed_data):
    decoder = byte_decoder.ByteDecoder()
    #delete key payload to assign to new name specific to message type
    payload = parsed_data['payload']
    print('payload:', payload)
    del parsed_data['payload']

    match parsed_data['id']:
        case MessageType.HAVE:
            parsed_data['piece_index'] = int.from_bytes(payload)
        
        case MessageType.BITFIELD:
            parsed_data['bitfield'] = payload

        case MessageType.REQUEST:
            print('initial data', parsed_data)
            print('bytes', payload[0: INT_PARAM_BYTES], payload[INT_PARAM_BYTES: 2*INT_PARAM_BYTES], payload[2*INT_PARAM_BYTES:])
            parsed_data['index'] = int.from_bytes(payload[0: INT_PARAM_BYTES])
            parsed_data['begin'] = int.from_bytes(payload[INT_PARAM_BYTES: 2*INT_PARAM_BYTES])
            parsed_data['length'] = int.from_bytes(payload[2*INT_PARAM_BYTES:])
            print('after data', parsed_data)

        case MessageType.PIECE:
            parsed_data['index'] = int.from_bytes(payload[LENGTH_BYTES+ID_BYTES: LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES])
            parsed_data['begin'] = int.from_bytes(payload[LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES: LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES])
            parsed_data['block'] = payload[LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES:]

        case MessageType.CANCEL:
            parsed_data['index'] = int.from_bytes(payload[LENGTH_BYTES+ID_BYTES: LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES])
            parsed_data['begin'] = int.from_bytes(payload[LENGTH_BYTES+ID_BYTES+INT_PARAM_BYTES: LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES])
            parsed_data['length'] = int.from_bytes(payload[LENGTH_BYTES+ID_BYTES+2*INT_PARAM_BYTES:])

        case MessageType.PORT:
            parsed_data['listen_port'] = int.from_bytes(payload)

    return parsed_data
    