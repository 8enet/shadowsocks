
mongodb_server = ('192.168.0.107', 27017)  # server:port
mongodb_dbname = 'py_db'
mongodb_auth = ('py_db1', 'admin1', 'SCRAM-SHA-1')  # dbuser , dbpwd ,mechanism

mongodb_access_log_doc_name = 'ss_access_log'

filter_user_port = [8383]   # filter special user,don't save log.
filter_access_port = [443]  # filter some encryp data port, e.g 443
filter_static_resource = []
