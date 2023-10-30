class TorrentStatistics:

    def __init__(self):
        self.downloaded_total = 0
        self.uploaded_total = 0
        self.downloaded_data = 0
        self.uploaded_data = 0
        self.downloaded_per_second = 0
        self.uploaded_per_second = 0

    def add_download(self, total_amount, data_amount=0):
        self.downloaded_total += total_amount
        self.downloaded_data += data_amount

    def add_upload(self, total_amount, data_amount=0):
        self.uploaded_total += total_amount
        self.uploaded_data += data_amount

    def get_download(self):
        return {
            'total': self.downloaded_total,
            'data': self.downloaded_data,
        }
    
    def get_upload(self):
        return {
            'total': self.uploaded_total,
            'data': self.uploaded_data,
        }

    def fetch_second_data(self):
        return {
            'download': self.downloaded_per_second,
            'upload': self.uploaded_per_second,
        }
    
    def __str__(self):
        return f'''Download total: {self.downloaded_total}
                Download data: {self.downloaded_data}
                Upload total: {self.uploaded_total}
                Upload data: {self.uploaded_data}'''