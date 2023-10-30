from datetime import datetime

class PeerStatus:
    
    def __init__(self):
        self.handshake_status = False
        self.choke_status = True
        self.connection_status = True
        self.interested_status = False
        self.last_message = datetime.now()

    def set_connection_status(self, status):
        self.connection_status = status

    def set_handshake_status(self, status):
        self.handshake_status = status

    def choke(self):
        self.choke_status = True

    def unchoke(self):
        self.choke_status = False

    def interested(self):
        self.interested_status = True

    def not_interested(self):
        self.interested_status = False

    def update_time(self):
        self.last_message = datetime.now()

    def get_handshake_status(self):
        return self.handshake_status

    def get_choke_status(self):
        return self.choke_status
    
    def get_interested_status(self):
        return self.interested_status
    
    def get_connection_status(self):
        return self.connection_status
    
    def get_time(self):
        return self.last_message