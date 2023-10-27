import math
import hashlib

class PieceTracker:

    def __init__(self, piece_hashes, piece_size):
        self.pieces = [None] * len(piece_hashes)
        self.piece_hashes = piece_hashes
        self.piece_size = piece_size

    def set_piece(self, index, data):
        if len(data) != self.piece_size:
            raise ValueError('Invalid chunk recieved')
        #seek to file location of index * piece_size + offset
        self.pieces[index] = data

    def get_bitfield(self):
        out_bytes = []
        for i in range(math.ceil(len(self.pieces) / 8)):
            current_byte = 0
            for bit_num in range(8):
                index = i * 8 + bit_num
                if not index >= len(self.pieces):
                    current_byte += (1 << 7 - bit_num) if self.pieces[index] else 0
            out_bytes.append(current_byte)
        return bytes(out_bytes)
    
    def remaining_pieces(self):
        return [i for i in range(len(self.pieces)) if not self.pieces[i]]
    
    def get_full_file(self):
        print(self.remaining_pieces())
        if self.remaining_pieces():
            return b''
        return b''.join(self.pieces)

if __name__ == '__main__':
    test = PieceTracker(100, 100)
    test.set_piece(69, b'testing')
    print(test.get_bitfield())
    print(test.remaining_pieces())
    for i in range(100):
        test.set_piece(i, b'abc')
    print(test.get_full_file())
    print(test.get_bitfield())