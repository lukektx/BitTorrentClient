import socket

HOST, PORT = "localhost", 6889

def message(id=0, payload=b''):
    if not id:
        return int(0).to_bytes(4, 'big')
    return (len(str(id)) + len(payload)).to_bytes(4, 'big') + id.to_bytes(1, 'big') + payload

data = message(None)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    sock.sendall(data)

    # Receive data from the server and shut down
    received = sock.recv(1024)

print(f"Sent:     {data}")
print(f"Received: {received}")  