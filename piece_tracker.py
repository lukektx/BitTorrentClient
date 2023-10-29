import math
import hashlib

HASH_SIZE = 20 #each has 20 bytes

class Block:
    def __init__(self,offset, length):
        self.start = offset
        self.end = offset + length - 1
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end

class Piece:
    def __init__(self, length):
        self.length = length
        self.current_blocks = []

    def have_block(self, offset, length):
        end = offset + length - 1
        for block in self.current_blocks:
            if offset >= block.get_start() and offset <= block.get_end():
                return True
            elif end >= block.get_start() and end <= block.get_end():
                return True
            elif offset <= block.get_start() and end >= block.get_end():
                return True
        return False

    def add_tracked_block(self, offset, length):
        self.current_blocks.append(Block(offset, length))

    def add_block(self, block, offset):
        if not self.data:
            self.data = bytearray(self.length)
        length = len(block)
        if not self.have_block:
            self.data[offset] = block
            self.add_tracked_block(offset, length)
            return True
        return False
    
    def get_length(self):
        return len(self.data)
    
    def get_request_offset(self):
        return self.request_offset
    
    def set_request_offset(self, offset):
        self.request_offset = offset
    
    def is_complete(self):
        return len(self.data) == self.length
    
class PieceTracker:

    def __init__(self, piece_hashes, piece_size, pieces):
        self.piece_hashes = piece_hashes
        self.piece_size = piece_size
        self.bitfield = Bitfield(pieces)
        self.pieces = [Piece(piece_size) for i in range(len(piece_hashes))]

    def get_piece(self, index):
        return self.bitfield[index // 8] & (1 << (7 - (index % 8)))

    def set_piece(self, index, offset, data):
        already_had = self.pieces[index].add_block(data, offset)
        if already_had:
            print('already had block')
        if self.pieces[index].is_complete():
            if self.check_hash(index):
                self.bitfield.set_piece_status(index)
                return True
            else:
                raise ValueError('Invalid piece hash')
            
        #block not complete yet
        return False
    
    def reset_piece(self, index):
        self.pieces[index] = Piece(self.piece_size)

    def check_hash(self, index):
        assert(self.pieces[index].get_length() != self.piece_size)
        # check against the 
        return hashlib.sha1(self.pieces[index]) == self.piece_hashes[index * HASH_SIZE:(index + 1) * HASH_SIZE]

    def get_bitfield(self):
        return self.bitfield
    
    def update_piece_request(self, index, offset, length):
        self.pieces[index].set_request_offset(offset + length)
    
    def num_downloaded_pieces(self):
        return sum([self.get_piece_status(index) for index in range(self.bitfield.length())])

    def remaining_pieces(self):
        out = []
        for index in range(self.bitfield.length()):
                if self.get_piece(index):
                    out.append(index)
        return out

class Bitfield:
    def __init__(self, pieces):
        self.bytes = bytearray(math.ceil(pieces / 8))

    def get_piece_status(self, index):
        return self.bitfield[index // 8] & (1 << (7 - (index % 8)))

    def set_piece_status(self, index):
        self.bitfield[index // 8] |= (1 << (7 - (index % 8)))

    def length(self):
        return len(self.bytes)

if __name__ == '__main__':
    test = PieceTracker(b'\xff' * 100, 100)
    test.set_piece(69, b'\xff')
    print(test.get_bitfield())
    print(test.remaining_pieces())
    for i in range(100):
        test.set_piece(i, b'abc')
    print(test.get_full_file())
    print(test.get_bitfield())