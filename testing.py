import utils.BEncode as Encoder
import utils.BDecode as Decoder

import locale

class Test:

    def __init__(self):
        self.encoder = Encoder.BEncode()
        self.decoder = Decoder.BDecode()

    def test(self, msg, test_input):
        encoded = self.encoder.encode(test_input)
        decoded = self.decoder.decode(encoded, current_index=[0])
        print(f'{'Passed' if decoded == test_input else f'Failed actaul: {decoded}, expected: {test_input}'} {msg}')

def str_tests():
    testing = Test()
    
    test_input = -1982378128
    testing.test('negative integer', test_input)

    test_input = 0
    testing.test('0 integer', test_input)

    test_input = 1234535
    testing.test('positive integer', test_input)

    test_input = ''
    testing.test('empty string', test_input)

    test_input = []
    testing.test('empty list', test_input)

    test_input = {}
    testing.test('empty dict', test_input)

    test_input = {'': [[{10: {}}]]}
    testing.test('empty nested structures', test_input)

    test_input = {
        123: ['bob', 'joe,', 'jeff'],
        "publisher-webpage": ["www.example.com", [1, 2, 3]], 
        "publisher.location": ['huh', 1, 2, ['a', 'b', [1, 2]]]
    }
    testing.test('nested structures', test_input)

if __name__ == '__main__':

    # test_decode = Decoder.BDecode()
    # test_encode = Encoder.BEncode()
    # with open('torrents//ubuntu-16.04-desktop-amd64.iso.torrent', 'rb') as f:
    #     meta_info = f.read()
    #     # print(meta_info[0])
    #     # print(type(meta_info))
    #     decoded = test_decode.decode(meta_info)
    #     print(decoded)
    #     encoded = test_encode.encode(decoded)
    pass