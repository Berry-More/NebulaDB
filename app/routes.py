from app import app

from flask import jsonify
from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool
from functions import class_correction


@app.route('/nebula/api/executes/<command>', methods=['GET'])
def make_execute(command):
    # connection
    config = Config()
    config.max_connection_pool_size = 10
    connection_pool = ConnectionPool()
    connection_pool.init([('127.0.0.1', 9669)], config)

    # get answer
    session = connection_pool.get_session('root', 'nebula')
    session.execute('use network;')
    answer = session.execute(command)
    dict_answer = {i: class_correction(answer.column_values(i)) for i in answer.keys()}
    if len(dict_answer) == 0:
        dict_answer = {'error': [None]}

    # close connection
    session.release()
    connection_pool.close()

    return jsonify(dict_answer)
