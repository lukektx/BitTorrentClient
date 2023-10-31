import socket
import sys

from . import message_decoder

LENGTH_BYTES = 4
ID_BYTES = 1
PSTR = b'BitTorrent protocol'
HANDSHAKE_LENGTH = 49 + len(PSTR)

class OwnConnection:

    def __init__(self, max_connections, ip, port):
        self.sock = self.peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_connections = max_connections
        self.ip = ip
        self.port = port

    def socket_connect(self):
        try:
            print((self.ip, self.port))
            self.sock.bind((self.ip, self.port))
            self.sock.listen(self.max_connections)
            print(f'Socket bound successfully to {self.ip}:{self.port}')
        except Exception as e:
            print('Error binding socket', e)
            sys.exit(0)

    def acquire_connection(self):
        peer = self.sock.accept()
        print('accepted connection')
        return peer

class PeerConnection:

    def __init__(self, connection, ip, port):
        self.peer_socket = connection
        self.ip = ip
        self.port = port

    def recieve_data(self, length):
        current_data = b''

        while length > 0:
            try:
                new_data = self.peer_socket.recv(length)
            except Exception as e:
                new_data = None
            if not new_data:
                return None
            current_data += new_data
            length -= len(new_data)

        return current_data

    def recieve_handshake(self):
        handshake = self.recieve_data(HANDSHAKE_LENGTH)
        if not handshake:
            print('invalid handshake recieved')
            return None
        pstrlen = int.from_bytes(handshake[0:1], 'big')
        print('pstrlen', pstrlen)
        if handshake[1:1+pstrlen] != PSTR:
            print('invalid PSTR in handshake')
            return None
        flags = handshake[1+pstrlen:9+pstrlen]
        info_hash = handshake[9+pstrlen:29+pstrlen]
        peer_id = handshake[29+pstrlen:]
        return {'flags':flags, 'info_hash':info_hash, 'peer_id':peer_id}

    def recieve_message(self):
        length = self.recieve_data(LENGTH_BYTES)
        # Connection closed or error with message
        if length == None:
            return None
        length = int.from_bytes(length, 'big')
        id = self.recieve_data(min(length, 1))
        if id == None:
            return None
        id = int.from_bytes(id) if id else -1
        payload = self.recieve_data(length - ID_BYTES)
        if payload == None:
            return None
        check_len = (len(payload) if payload else 0) + (1 if id != -1 else 0)
        if(check_len != length):
            #TODO handle invalid transmission (length != expected_len)
            print('invalid message (length != data recieved)')
            return None
        return message_decoder.extract_payload({'length': length, 'id': id, 'payload': payload})

    def send_data(self, data):
        try:
            self.peer_socket.sendall(data)
        except Exception as e:
            print('Failed to send all data', e)
            raise e
    
class PeerDownload(PeerConnection):
    def __init__(self, ip, port):
        new_socket = socket.Socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__(new_socket, ip, port)

    def socket_connect(self):
        socket.connect((self.ip, self.port))

if __name__ == '__main__':
    HOST, PORT = "localhost", 6889
    find = OwnConnection(1, HOST, PORT)
    find.socket_connect()
    conn, addr = find.acquire_connection()
    ip, port = addr
    test = PeerConnection(conn, ip, port)
    print(test.recieve_block(1000))