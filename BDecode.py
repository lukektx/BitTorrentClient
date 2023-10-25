class BDecode:

    def decode(self, encoded, current_index=[0]):

        while current_index[0] < len(encoded):
            current_token = encoded[current_index[0]]
            match current_token:
                case 'i':
                    start_index = current_index[0] + 1
                    current_index[0] = encoded.find('e', start_index)
                    return int(encoded[start_index: current_index[0]])

                case 'l':
                    out = []
                    while (encoded[current_index] != 'e'):
                        current_index[0] += 1
                        out.append(self.decode(encoded, current_index))

                case 'd':
                    out = {}
                    while (encoded[current_index[0]] != 'e'):
                        current_index[0] += 1
                        key = self.decode(encoded, current_index)
                        current_index[0] += 1
                        value = self.decode(encoded, current_index)
                        out[key] = value
                    return out
                
                case _:
                    start_index = current_index[0] + 1
                    current_index[0] = encoded.find(':', start_index)
                    length = int(encoded[start_index: current_index[0]])
                    start_index = current_index[0] + 1
                    current_index[0] = start_index + length + 1
                    return encoded[start_index: current_index[0]]



if __name__ == '__main__':
    test = BDecode()
    test_input = f'd3:cow3:moo4:spam4:eggse'
    print(test.decode(test_input))
