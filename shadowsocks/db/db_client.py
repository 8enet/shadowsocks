from pymongo import MongoClient
from shadowsocks import control_config as db_config
import time


global _db
client = MongoClient(db_config.mongodb_server[0], db_config.mongodb_server[1])[db_config.mongodb_dbname]
client.authenticate(db_config.mongodb_auth[0], db_config.mongodb_auth[1],
                    mechanism=db_config.mongodb_auth[2])
_db = client[db_config.mongodb_access_log_doc_name]


def insert(bean):
    try:
        if need_filter(bean):
            doc = {'u_p': bean.userPort, 'h': bean.hostname, 'h_p': bean.port,
                   'hed': bean.headers if bean.port not in db_config.filter_access_port else '',
                   't': int(time.time())}
            res = _db.insert_one(doc)
            print(res)
    except Exception as e:
        print(e)
        pass


def find():
    return _db.find()

def need_filter(bean):
    if bean.userPort not in db_config.filter_user_port:
        return False
    for res in db_config.filter_static_resource:
        print(res)
        if str(bean.headers).index(res) is not -1:
            return False
    return True

def delete():
    _db.delete_many({})

def test():
    log = AccessLog()
    log.port = 80
    log.hostname = 'www.baidu.com'
    log.userPort = 8891
    log.headers = b"""
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding:gzip, deflate, sdch
    Accept-Language:zh-CN,zh;q=0.8
    Connection:keep-alive
    DNT:1
    Host:www.baidu.com
    Upgrade-Insecure-Requests:1
    User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36
    """
    insert(log)
    for item in find():
        print(item)
    # delete()
    pass



def test2():
    text = b"""
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding:gzip, deflate, sdch
    Accept-Language:zh-CN,zh;q=0.8
    Connection:keep-alive
    DNT:1
    Host:www.baidu.com
    Upgrade-Insecure-Requests:1
    User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36
    """
    print(len(text))
    print(type(text))
    now = time.time()
    for i in range(0,100000):
        text.index(b'Apple')
    print('time  %s ' % (time.time()-now))
    pass


class AccessLog(object):
    def __init__(self):
        self.hostname = None  # access host server name
        self.port = 80        # access host port
        self.headers = None   # header
        self.userPort = None  # user link port


if __name__ == '__main__':
    test2()
