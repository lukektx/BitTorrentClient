import client
import threading

TORRENT_FILE = 'torrents//ubuntu-23.10.1-desktop-amd64.iso.torrent'
OUT_PATH = 'out'
IN_PATH = 'C://Users//lukek//Downloads'

def seed():
    print('seed')
    client.Client(TORRENT_FILE, IN_PATH, operation='seed').loop()

if __name__ == '__main__':
    print('test')
    seeding = threading.Thread(target=seed)
    seeding.start()
    seeding.join()