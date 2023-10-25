class BDecode:
    def decode(self, encoded, current_index=[0]):

        while current_index[0] < len(encoded):
            current_token = encoded[current_index[0]]
            match current_token:
                case 'i':
                    start_index = current_index[0] + 1
                    end_index = encoded.find('e', start_index)
                    current_index[0] = end_index + 1
                    return int(encoded[start_index: end_index])

                case 'l':
                    out = []
                    current_index[0] += 1
                    while (encoded[current_index[0]] != 'e'):
                        out.append(self.decode(encoded, current_index))
                    current_index[0] += 1
                    return out

                case 'd':
                    out = {}
                    current_index[0] += 1

                    while (encoded[current_index[0]] != 'e'):
                        key = self.decode(encoded, current_index)
                        value = self.decode(encoded, current_index)
                        out[key] = value
                    current_index[0] += 1
                    return out
                
                case _:
                    start_index = current_index[0]
                    current_index[0] = encoded.find(':', start_index)
                    length = int(encoded[start_index: current_index[0]])
                    start_index = current_index[0] + 1
                    current_index[0] = start_index + length
                    return encoded[start_index: current_index[0]]



if __name__ == '__main__':
    test = BDecode()
    test_input = f'di123el3:bob4:joe,4:jeffe17:publisher-webpagel15:www.example.comli1ei2ei3eee18:publisher.locationl3:huhi1ei2el1:a1:bli1ei2eeeee'
    print(test.decode(test_input))
