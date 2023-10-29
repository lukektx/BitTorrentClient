import threading

class DownloadQueue:

    def __init__(self):
        self.lock = threading.Lock()
        self.queue = []
        self.strict_priority = False

    def set_queue(self, queue):
        self.lock.acquire()
        self.queue = queue
        self.lock.release()

    def enable_strict_priority(self):
        self.lock.acquire()
        self.strict_priority = True
        self.lock.release()

    def disable_strict_priority(self):
        self.lock.acquire()
        self.strict_priority = False
        self.lock.release()

    def get_needed_piece(self):
        self.lock.acquire()
        if self.strict_priority:
            piece_index =  self.queue[-1]
        else:
            piece_index =  self.queue.pop()
        self.lock.release()
        return piece_index
    
    def remove_piece(self, piece):
        self.lock.acquire()
        if piece in self.queue:
            self.queue.remove(piece)
        self.lock.release()
