from pymongo import MongoClient
from shadowsocks import control_config as db_config
from bson.objectid import ObjectId
from shadowsocks import accesslog
import json
import re
import time


global _db
client = MongoClient(db_config.mongodb_server[0], db_config.mongodb_server[1])[db_config.mongodb_dbname]
client.authenticate(db_config.mongodb_auth[0], db_config.mongodb_auth[1],
                    mechanism=db_config.mongodb_auth[2])
_db = client[db_config.mongodb_access_log_doc_name]


def insert(bean):
    try:
        if _need_filter(bean):
            doc = {'u_p': bean.userPort, 'h': bean.hostname, 'h_p': bean.port,
                   'hed': str(bean.headers) if bean.port not in db_config.filter_access_port else '',
                   't': int(time.time())}
            res = _db.insert_one(doc)
    except Exception as e:
        print(e)
        pass

def get_size(bean=None):
    return _db.count(_parse2condition(bean))

def findAll():
    """
    查询所有
    :return:
    """
    return _db.find()


def find_by_id(_id):
    """
    查询单个
    :param _id:
    :return:
    """
    return _db.find_one({"_id": ObjectId(_id)})

def find_by_map(bean):
    # rgx = re.compile('.*.baidu.com*', re.IGNORECASE)
    print(_parse2condition(bean))
    return _db.find(_parse2condition(bean))


def get_dataofpage(offset, pagesize=10, bean=None):
    """
    分页查询
    :param offset:
    :param pagesize:
    :return:
    """
    cond = {}
    if bean:
        cond = _parse2condition(bean)
    return _db.find(cond).skip(offset).limit(pagesize)


def deleteAll():
    return _db.delete_many({})


def delete_by_id(_id):
    return _db.delete_one({"_id": ObjectId(_id)})

def delete_by_map(bean):
    return _db.delete_many(_parse2condition(bean))

def _parse2condition(bean):
    if bean is None:
        return {}

    dits = {}
    cons = []
    if bean.hostname:
        cons.append({"h": re.compile(r'' + bean.hostname + '', re.IGNORECASE)})

    if bean.headers:
        cons.append({'hed': re.compile(r''+bean.headers+'', re.IGNORECASE)})

    if len(cons) is not 0:
        dits["$or"] = cons

    cons = []
    if bean.userPort is not 0:
        cons.append({"u_p": bean.userPort})
    if bean.port is not 0:
        cons.append({"h_p": bean.port})
    if len(cons) is not 0:
        dits["$and"] = cons
    return dits



def _need_filter(bean):
    if bean.userPort in db_config.filter_user_port:
        return False
    for res in db_config.filter_static_resource:
        if str(bean.hostname).find(res) is not -1 or str(bean.headers).find(res) is not -1:
            return False
    return True

def test():
    nt = time.time()
    log = accesslog.AccessLog()
    log.hostname = 'tieba.baidu.com'
    log.headers = 'tieba.'
    log.userPort = 8381
    log.port = 80

    # for item in find_by_map(log):
    #     print(item)
    #delete()

    #delete_by_map(log)

    print(get_size(log))

    print(list(get_dataofpage(0,2,log)))
    print("---------")
    print(list(get_dataofpage(2,2,log)))

    print('use time  -->> %s ' % (time.time()-nt))
    pass


if __name__ == '__main__':
    test()
