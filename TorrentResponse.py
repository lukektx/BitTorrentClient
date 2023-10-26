from utils import BDecode as Decode

class TrackerResponse:

    def __init__(self, response):
        self.decoder = Decode.BDecode()
        self.responose = response

    def get_peers(self):
        