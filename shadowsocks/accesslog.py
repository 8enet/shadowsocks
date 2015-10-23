
class AccessLog(object):
    def __init__(self):
        self.id = None
        self.hostname = None  # access host server name
        self.port = 80        # access host port
        self.headers = None   # header
        self.userPort = None  # user link port

    def __repr__(self):
        return 'from %s -> %s:%s%s' % (self.userPort, self.hostname, self.port, str(self.headers) if self.port is not 443 else '')


def parse_bean(doc):
    log = AccessLog()
    log.id = str(doc['_id'])
    log.hostname = doc['h']
    log.port = doc['h_p']
    log.headers = str(doc['hed'])
    log.userPort = doc['u_p']
    return log