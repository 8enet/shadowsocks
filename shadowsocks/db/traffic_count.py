import socket
import logging
import time
import redis
from hurry.filesize import size

from shadowsocks import common


r = redis.StrictRedis(host='192.168.0.107', port=6379, db=0)

def traffic_add(user_port, data_len):
    key = 'user-%s' % user_port
    count = int(common.to_str(r.incr(key, data_len)))
    if count > 329289379:
        print('close port ')
        close_user_port(user_port)

def test():
    res = r.get('user-8388')
    print(int(res.decode('utf-8')))
    print(size(int(res.decode('utf-8'))))
    print(size(329289379))

def close_user_port(user_port):
    cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.error('start close conn .. ')
    cli.connect(('127.0.0.1', 55055))
    time.sleep(5)
    cli.send(b'ping')
    print(cli.recv(1506))
    logging.error('send close cmd .. ')
    cli.send(b'remove: {"server_port":8838}')
    data = cli.recv(1506)
    print('rec data %s  ' % (common.to_str(data)))
    assert b'ok' in data

if __name__ == '__main__':
    test()
