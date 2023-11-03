class NetworkManager:

    def __init__(self, statistics):
        self.statistics = statistics
        self.outgoing_requests = 0
        self.send_queue = []

    def queue(self, message):
        self.send_queue.append(message)

    def 