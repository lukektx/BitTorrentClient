class BEncode:
    def __init__(self):
        self.type_mapping = {
            int: self.int_encode,
            str: self.str_encode,
            list: self.list_encode,
            dict: self.dict_encode,
        }

    @staticmethod
    def byte_encode(data):
        return bytes(data, 'utf-8')

    def encode(self, data):
        try:
            data = data.decode('utf-8') if type(data) == bytes else data
        except UnicodeDecodeError:
            return self.bytes_encode(data)
        if not type(data) in self.type_mapping:
            raise Exception(f'No encoding defined for type: {type(data)}')
        return self.type_mapping[type(data)](data)

    def int_encode(self, data):
        return self.byte_encode(f'i{data}e')

    def str_encode(self, data):
        return self.byte_encode(f'{len(data)}:{data}')

    def list_encode(self, data):
        list_represntation = [self.encode(elem) for elem in data]
        list_represntation.insert(0, b'l')
        list_represntation.append(b'e')
        return b''.join(list_represntation)

    def dict_encode(self, data):
        dict_represntation = [self.encode(key) + self.encode(data[key]) for key in data]
        dict_represntation.insert(0, b'd')
        dict_represntation.append(b'e')
        return b''.join(dict_represntation)

    def bytes_encode(self, data):
        return self.byte_encode(str(len(data))) + b':' + data

if __name__ == '__main__':

    test = BEncode()
    test_input = {'': [[{}]]}

    print(test.encode(test_input))
