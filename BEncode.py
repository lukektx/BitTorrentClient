class BEncode:
    def __init__(self):
        self.type_mapping = {
            int: self.int_encode,
            str: self.str_encode,
            list: self.list_encode,
            dict: self.dict_encode
        }

    def encode(self, data):
        if not type(data) in self.type_mapping:
            raise Exception(f'No encoding defined for type: {type(data)}')
        return self.type_mapping[type(data)](data)

    @staticmethod
    def int_encode(data):
        return f'i{data}e'

    @staticmethod
    def str_encode(data):
        return f'{len(data)}:{data}'

    def list_encode(self, data):
        list_represntation = [self.encode(elem) for elem in data]
        list_represntation.insert(0, 'l')
        list_represntation.append('e')
        return ''.join(list_represntation)

    def dict_encode(self, data):
        dict_represntation = [self.encode(
            key) + self.encode(data[key]) for key in data]
        dict_represntation.insert(0, 'd')
        dict_represntation.append('e')
        return ''.join(dict_represntation)


if __name__ == '__main__':

    test = BEncode()
    test_input = {"publisher": "bob",
                  "publisher-webpage": "www.example.com", "publisher.location": "home"}
    print(type(test_input))
    print(test.encode(test_input))
