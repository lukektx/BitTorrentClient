import threading

class FileHandler:

    def __init__(self, file_path):
        self.file = open(file_path, 'ab+')
        self.lock = threading.Lock()

    def read(self, offset, length):
        self.lock.acquire()
        self.file.seek(offset)
        data = self.file.read(length)
        self.lock.release()
        return data
    
    def write(self, offset, data):
        self.lock.acquire()
        self.file.seek(offset)
        self.file.write(data)
        self.lock.release()
