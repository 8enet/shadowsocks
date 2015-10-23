class AccessRecord(object):
    def __init__(self):
        self.hostname = None  # access host server name
        self.port = 80        # access host port
        self.headers = None   # header
        self.userPort = None  # user link port