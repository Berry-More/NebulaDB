from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool

import time


def make_execute(message):
    # connection
    config = Config()
    config.max_connection_pool_size = 10
    connection_pool = ConnectionPool()
    connection_pool.init([('127.0.0.1', 9669)], config)

    # get answer
    session = connection_pool.get_session('root', 'nebula')
    session.execute('use network;')
    answer = session.execute(message)
    dict_answer = {i: answer.column_values(i) for i in answer.keys()}

    # close connection
    session.release()
    connection_pool.close()

    return dict_answer

