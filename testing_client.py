import socket
import time
from utils import messages
import torrent
from enum import IntEnum

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

HOST, PORT = "localhost", 6889

def message(id=0, payload=b''):
    if not id:
        return int(0).to_bytes(4, 'big')
    return (len(str(id)) + len(payload)).to_bytes(4, 'big') + id.to_bytes(1, 'big') + payload

data = messages.request(0, 0, 2 ** 14)

HANDLER_ACTIONS = {
    10: messages.handshake,
    MessageType.KEEP_ALIVE: messages.keep_alive,
    MessageType.CHOKE: messages.choke,
    MessageType.UNCHOKE: messages.unchoke,
    MessageType.INTERESTED: messages.interested,
    MessageType.NOT_INTERESTED: messages.not_interested,
    MessageType.HAVE: messages.have,
    MessageType.BITFIELD: messages.bitfield,
    MessageType.REQUEST: messages.request,
    MessageType.PIECE: messages.piece,
    MessageType.CANCEL: messages.cancel,
    MessageType.PORT: messages.port,
}
def get_message(message_info):
    args = message_info.split(' ')
    args = [int(args[i]) for i in range(len(args))]
    if args[0] == 10:
        args.append(my_torrent.info_hash())
        args.append(my_torrent.id)
    print(args[1:])
    match(len(args[1:])):
        case 0:
            return HANDLER_ACTIONS[args[0]]()
        case 1:
            return HANDLER_ACTIONS[args[0]](args[1])
        case 2:
            return HANDLER_ACTIONS[args[0]](args[1], args[2])
        case 3:
            return HANDLER_ACTIONS[args[0]](args[1], args[2], args[3])

TORRENT_FILE = 'torrents//ubuntu-23.10.1-desktop-amd64.iso.torrent'
OUT_PATH = 'out'
IN_PATH = 'C://Users//lukek//Downloads'

my_torrent = torrent.Torrent(TORRENT_FILE, OUT_PATH, 19848, 50, 'download')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(get_message('10'))
    while True:
        message_info = input('what message do you want to send?\n')
        data = get_message(message_info)
        sock.sendall(data)
        print(f'sent: {data}')

        args = message_info.split(' ')
        args = [int(args[i]) for i in range(len(args))]

        # Receive data from the server and shut down
        recived = b''
        if args[0] == 6:
            received = sock.recv(9 + args[3])
        elif args[0] == -1:
            pass
        else: 
            received = sock.recv(len(data))
        print(f"Received: {received}")