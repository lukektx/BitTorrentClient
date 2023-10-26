class BDecode:

    def __init__(self):
        self.int_match = ord('i')
        self.list_match = ord('l')
        self.dict_match = ord('d')
        self.end_match = ord('e')
        self.delimeter_match = ord(':')

    def decode(self, encoded, current_index=[0]):

        while current_index[0] < len(encoded):
            current_token = encoded[current_index[0]]
            match current_token:
                case self.int_match:
                    start_index = current_index[0] + 1
                    end_index = encoded.find(b'e', start_index)
                    current_index[0] = end_index + 1
                    return int(encoded[start_index: end_index])

                case self.list_match:
                    out = []
                    current_index[0] += 1
                    while (encoded[current_index[0]] != self.end_match):
                        out.append(self.decode(encoded, current_index))
                    current_index[0] += 1
                    return out

                case self.dict_match:
                    out = {}
                    current_index[0] += 1
                    while (encoded[current_index[0]] != self.end_match):
                        key = self.decode(encoded, current_index)
                        value = self.decode(encoded, current_index)
                        out[key] = value
                    current_index[0] += 1
                    return out
                
                case _:
                    start_index = current_index[0]
                    current_index[0] = encoded.find(self.delimeter_match, start_index)
                    length = int(encoded[start_index: current_index[0]])
                    start_index = current_index[0] + 1
                    current_index[0] = start_index + length
                    
                    return encoded[start_index: current_index[0]]



if __name__ == '__main__':
    test = BDecode()
    test_input = f'di123el3:bob4:joe,4:jeffe17:publisher-webpagel15:www.example.comli1ei2ei3eee18:publisher.locationl3:huhi1ei2el1:a1:bli1ei2eeeee'
    print(test.decode(test_input))
