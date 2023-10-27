import math
import hashlib

class PieceTracker:

    def __init__(self, piece_hashes, piece_size):
        self.piece_hashes = piece_hashes
        self.piece_size = piece_size
        self.bitfield = bytearray(math.ceil(len(piece_hashes) / 8))
        print(self.bitfield)

    def get_piece(self, index):
        return self.bitfield[index // 8] & (1 << (7 - (index % 8)))

    def set_piece(self, index):
        self.bitfield[index // 8] |= (1 << (7 - (index % 8)))

    def set_data(self, index, data):
        if len(data) != self.piece_size:
            raise ValueError('Invalid chunk recieved')
        # if hashlib.sha1(data).digest(4) != 
        #seek to file location of index * piece_size + offset
        self.pieces[index] = data

    def get_bitfield(self):
        return self.bitfield
    
    def remaining_pieces(self):
        out = []
        for index, byte in enumerate(self.bitfield):
            for bit_num in range(8):
                if self.get_piece(index * 8 + bit_num):
                    out.append(index * 8 + bit_num)
        return out

if __name__ == '__main__':
    test = PieceTracker(b'\xff' * 100, 100)
    test.set_piece(69)
    print(test.get_bitfield())
    print(test.remaining_pieces())
    for i in range(100):
        test.set_piece(i, b'abc')
    print(test.get_full_file())
    print(test.get_bitfield())