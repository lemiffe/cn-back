# Note: Run with python 3

# Standard libraries
import time
import logging
import configparser
import sys
import os
import os.path
import json
import pickle

# External libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
import tornado.web
import tornado.autoreload
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging

# Set up Flask/Tornado
app = Flask(__name__)
app.debug = True
CORS(app)
limiter = Limiter(app)

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')
environment = config['server']['environment']
if environment is None or environment == '':
    environment = 'production'

# Set up logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
if environment == 'production':
    logger.setLevel(logging.ERROR)


@app.route('/', methods=['POST', 'DELETE', 'GET'])
@limiter.limit("1000/hour", key_func = lambda : 'current_user.username') # TODO use ip+user combination
def index():
    # Get variables
    #content = request.json
    #if content is None:
    #    return make_error('JSON body not sent', 400)
    #if 'tree_id' not in content:
    #    return make_error('Tree ID (tree_id) not sent (or incorrect format)', 400)
    #tree_id = int(content['tree_id'])

    try:
        if request.method == 'POST':
            return success({"msg": "hi POST"})
        elif request.method == 'DELETE':
            return success({"msg": "hi DELETE"})
        elif request.method == 'GET':
            return success({"msg": "hi GET"})
    except KeyError as inst:
        if request.method == 'DELETE':
            return error_not_found(inst)
        return make_error(inst, 409)
    except Exception as inst:
        return make_error(inst, 409)


def success(obj):
    response = {
        'meta': {
            'code': '200',
            'message': 'OK',
        },
        'response': obj
    }
    response = jsonify(response)
    response.status_code = 200
    return response


@app.errorhandler(404)
def error_not_found(error=None):
    output_error = 'Resource not found.'
    if error is not None:
        if isinstance(error, basestring):
            output_error = error
        else:
            try:
                output_error += ' ' + str(error.description)
            except Exception as inst:
                output_error += ' ' + str(inst)
    return make_error(output_error, 404)


@app.errorhandler(500)
def error_unknown(error=None):
    output_error = 'Internal server error. We have caught this and will work to fix this issue ASAP.'
    # TODO: If on production environment don't do the following
    if error is not None:
        if isinstance(error, basestring):
            output_error = error
        else:
            try:
                output_error += ' ' + str(error.description)
            except Exception as inst:
                output_error += ' ' + str(inst)
    return make_error(output_error, 500)


def make_error(msg, code):
    response = {
        'meta': {
            'code': int(code),
            'message': str(msg),
        },
        'response': None
    }
    response = jsonify(response)
    response.status_code = code
    return response


if __name__ == '__main__':   
    
    if environment == 'production':
        # Run Tornado server
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(port)
        IOLoop.instance().start()

    else:
        # Run Flask server
        app.run(debug=True, host='0.0.0.0', port=8080)
