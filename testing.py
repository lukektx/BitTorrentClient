import BEncode as Encoder
import BDecode as Decoder

class Test:

    def __init__(self):
        self.encoder = Encoder.BEncode()
        self.decoder = Decoder.BDecode()

    def test(self, msg, test_input):
        encoded = self.encoder.encode(test_input)
        decoded = self.decoder.decode(encoded, current_index=[0])
        print(f'{'Passed' if decoded == test_input else f'Failed actaul: {decoded}, expected: {test_input}'} {msg}')

if __name__ == '__main__':

    testing = Test()
    
    test_input = {'': [[{10: {}}]]}

    testing.test('empty nested structures', test_input)

    test_input2 = {
        123: ['bob', 'joe,', 'jeff'],
        "publisher-webpage": ["www.example.com", [1, 2, 3]], 
        "publisher.location": ['huh', 1, 2, ['a', 'b', [1, 2]]]
    }

    testing.test('nested structures', test_input2)
