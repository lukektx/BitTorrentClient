import math
import hashlib

HASH_SIZE = 20 #each has 20 bytes

class Piece:
    def __init__(self, length):
        self.data = bytearray()
        self.length = length

    def add_block(self, block):
        self.data.append(block)
    
    def get_length(self):
        return len(self.data)
    
    def is_complete(self):
        return len(self.data) == self.length
    
class PieceTracker:

    def __init__(self, piece_hashes, piece_size, pieces):
        self.piece_hashes = piece_hashes
        self.piece_size = piece_size
        self.bitfield = Bitfield(pieces)
        self.pieces = [Piece() for i in range(len(piece_hashes))] 

    def get_piece(self, index):
        return self.bitfield[index // 8] & (1 << (7 - (index % 8)))

    def set_piece(self, index, data):
        self.pieces[index].add_block(data)
        if self.pieces[index].is_complete():
            if self.check_hash(index):
                self.bitfield.set_piece_status(index)
                return True
            else:
                print('Invalid piece hash')
                return False
            
        #block not complete yet
        return False

    def check_hash(self, index):
        assert(self.pieces[index].get_length() != self.piece_size)
        # check against the 
        return hashlib.sha1(self.pieces[index]) == self.piece_hashes[index * HASH_SIZE:(index + 1) * HASH_SIZE]

    def get_bitfield(self):
        return self.bitfield
    
    def remaining_pieces(self):
        out = []
        for index, byte in enumerate(self.bitfield):
            for bit_num in range(8):
                if self.get_piece(index * 8 + bit_num):
                    out.append(index * 8 + bit_num)
        return out

class Bitfield:
    def __init__(self, pieces):
        self.bytes = bytearray(math.ceil(pieces / 8))

    def get_piece_status(self, index):
        return self.bitfield[index // 8] & (1 << (7 - (index % 8)))

    def set_piece_status(self, index):
        self.bitfield[index // 8] |= (1 << (7 - (index % 8)))

if __name__ == '__main__':
    test = PieceTracker(b'\xff' * 100, 100)
    test.set_piece(69, b'\xff')
    print(test.get_bitfield())
    print(test.remaining_pieces())
    for i in range(100):
        test.set_piece(i, b'abc')
    print(test.get_full_file())
    print(test.get_bitfield())