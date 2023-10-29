import torrent

class Client:

    def __init__(self, torrent_file, out_path, port=6889, max_peers=50, operation='download'):
        self.torrent = torrent.Torrent(torrent_file, out_path, port, max_peers, operation)
        self.operation = operation

    def download(self,):
        self.torrent.find_peers()
        self.torrent.connect_peers()
        self.torrent.download()
        print('finished downloading')

    def seed(self):
        self.torrent.begin_seeding()

    def loop(self):
        if self.operation == 'download':
            self.download()
        elif self.operation == 'seed':
            self.seed()

if __name__ == '__main__':
    test = Client
    (
        'torrents//ubuntu-23.10.1-desktop-amd64.iso.torrent',
        
    )
    