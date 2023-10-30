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
    
    def get_data(self):
        return bytes(self.data)
    
    def is_complete(self):
        return len(self.data) == self.length
    
class PieceTracker:

    def __init__(self, file_handler, piece_hashes, piece_size, pieces):
        self.file_handler = file_handler
        self.piece_hashes = piece_hashes
        self.piece_size = piece_size
        self.bitfield = Bitfield(pieces)
        self.pieces = [Piece(piece_size) for i in range(len(piece_hashes))]

    def get_bitfield_status(self, index):
        return self.bitfield.get_piece_status(index)
    
    def set_bitfield_status(self, index):
        self.bitfield.set_piece_status(index)

    def get_piece(self, index):
        return self.get_block(index, 0, self.piece_size)

    def get_block(self, index, begin, length):
        return self.file_handler.read(index * self.piece_size + begin, length)

    def set_block(self, index, offset, data):
        already_had = self.pieces[index].add_block(data, offset)
        if already_had:
            print('already had block')
        if self.pieces[index].is_complete():
            print('completed block', index)
            if self.check_hash(index):
                self.bitfield.set_piece_status(index)
                self.file_handler.write(index * self.piece_size + offset, self.pieces[index])
                self.pieces[index] = Piece(self.piece_size)
                return True
            else:
                raise ValueError('Invalid piece hash')
            
        #block not complete yet
        return False
    
    def reset_piece(self, index):
        self.pieces[index] = Piece(self.piece_size)

    def check_hash(self, index, disk=False):
        data = b''
        if not disk:
            assert(self.pieces[index].get_length() != self.piece_size)
            data = self.pieces[index]
        else:
            data = self.get_piece(index)

        return hashlib.sha1(data).digest() == self.piece_hashes[index * HASH_SIZE:(index + 1) * HASH_SIZE]

    def get_bitfield(self):
        return self.bitfield
    
    def num_downloaded_pieces(self):
        print('bitfield length', self.bitfield.length())
        return sum([self.get_bitfield_status(index) for index in range(self.bitfield.length())])

    def remaining_pieces(self):
        out = []
        for index in range(self.bitfield.length()):
                if self.get_bitfield_status(index):
                    out.append(index)
        return out

class Bitfield:
    def __init__(self, pieces):
        self.bytes = bytearray(pieces)

    def get_piece_status(self, index):
        return self.bytes[index // 8] >> (7 - (index % 8)) & 1

    def set_piece_status(self, index):
        self.bytes[index // 8] |= (1 << (7 - (index % 8)))

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