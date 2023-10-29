import socket
import sys

from utils import message_decoder

LENGTH_BYTES = 4
ID_BYTES = 1

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
                print('socket closed?')
                return None
            current_data += new_data
            length -= len(new_data)

        return current_data

    def recieve_message(self):
        length = int.from_bytes(self.recieve_data(LENGTH_BYTES))
        id = int.from_bytes(self.recieve_data(ID_BYTES))
        payload = self.recieve_data(length - ID_BYTES)
        if(ID_BYTES + len(payload) != length):
            #TODO handle invalid transmission (length != expected_len)
            return
        return message_decoder.parse_data({'length': length, 'id': id, 'payload': payload})

    def send_data(self, data):
        try:
            self.peer_socket.sendll(data)
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