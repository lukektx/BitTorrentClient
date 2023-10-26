class Metadata:

    def __init__(self):
        self.type_mapping = {
            bytes: self.bytes_decode,
            int: self.int_decode,
            list: self.list_decode,
            dict: self.dict_decode
        }

    def bytes_decode(self, data):
        try:
            decoded = data.decode('utf-8')
            return decoded
        except UnicodeDecodeError:
            return data
        
    def int_decode(self, data):
        return data

    def list_decode(self, data):
        return [self.bytes_to_str(elem) for elem in data]
    
    def dict_decode(self, data):
        out = {}
        for key in data:
              out[self.bytes_to_str(key)] = self.bytes_to_str(data[key])
        return out

    def bytes_to_str(self, data):
        return self.type_mapping[type(data)](data)