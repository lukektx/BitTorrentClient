import socket
import sys

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

    def socket_connect(self):
        try:
            self.peer_socket.bind((self.ip, self.port))
            self.peer_socket.listen()
        except Exception as e:
            print('Error binding socket', e)
            sys.exit(0)

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

    def send_data(self, data):
        try:
            self.peer_socket.sendll(data)
        except Exception as e:
            print('Failed to send all data', e)
            raise e

    def acquire_connection(self):
        return self.peer_socket.accept()
    
if __name__ == '__main__':
    HOST, PORT = "localhost", 6889
    find = OwnConnection(1, HOST, PORT)
    find.socket_connect()
    conn, addr = find.acquire_connection()
    ip, port = addr
    test = PeerConnection(conn, ip, port)
    print(test.recieve_block(1000))