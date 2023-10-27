import math
import hashlib

class Piece:
    def __init__(self):
        self.data = bytearray()

    def add_block(self, block):
        self.data.append(block)
    
    def get_length(self):
        return len(self.data)

class PieceTracker:

    def __init__(self, piece_hashes, piece_size):
        self.piece_hashes = piece_hashes
        self.piece_size = piece_size
        self.bitfield = bytearray(math.ceil(len(piece_hashes) / 8))
        self.pieces = [Piece() for i in range(len(piece_hashes))] 

    def get_piece(self, index):
        return self.bitfield[index // 8] & (1 << (7 - (index % 8)))

    def set_piece(self, index, data):
        self.pieces[index].add_block(data)
        self.bitfield[index // 8] |= (1 << (7 - (index % 8)))

    def check_hash(self, index):
        assert(self.pieces[index].get_length() != self.piece_size)
        # check against the 
        return hashlib.sha1(self.pieces[index]) == self.piece_hashes[index * 20:(index + 1) * 20]

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
    test.set_piece(69, b'\xff')
    print(test.get_bitfield())
    print(test.remaining_pieces())
    for i in range(100):
        test.set_piece(i, b'abc')
    print(test.get_full_file())
    print(test.get_bitfield())