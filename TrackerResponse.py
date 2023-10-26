from utils import BDecode as Decode
from utils import ByteDecoder

class TrackerResponse:

    def __init__(self, response):
        self.HOST_LEN = 4
        self.PORT_LEN = 2
        self.PEER_LEN = 6
        self.decoder = Decode.BDecode()
        self.response = response
        self.decoded_response = self.decoder.decode(response, current_index=[0])

    def get_peers(self):
        print(self.decoded_response)
        raw_peers = self.decoded_response['peers']
        peers  = []
        for i in range(len(raw_peers) // self.PEER_LEN):
            current_peer = raw_peers[i * self.PEER_LEN : (i + 1) * self.PEER_LEN]
            host = '.'.join([str(byte) for byte in current_peer[0:self.HOST_LEN]])
            port = str(int.from_bytes(current_peer[self.HOST_LEN: self.PEER_LEN], byteorder='big'))
            peers.append(f'{host}:{port}')
        return peers