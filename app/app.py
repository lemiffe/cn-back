# Standard libraries
import time
import logging
import configparser
import sys
import os
import os.path
import json
import pickle
from functools import wraps

# External libraries
from flask import Flask, jsonify, request, _request_ctx_stack
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
import tornado.web
import tornado.autoreload
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from six.moves.urllib.request import urlopen
from jose import jwt
import urllib.parse

# Controllers
from controllers.UserController import UserController
from controllers.ErrorController import ErrorController

# Set up Flask/Tornado
app = Flask(__name__)
app.debug = True
CORS(app)
limiter = Limiter(app)

# Set up controllers
user_controller = UserController(app)
error_controller = ErrorController(app)

# Read configuration file
config = configparser.ConfigParser()
config.read('config.ini')
environment = config['server']['environment']
if environment is None or environment == '':
    environment = 'production'

# Auth0 config
auth0_domain = config['auth0']['domain']
auth0_audience = config['auth0']['audience']
auth0_algorithms = [config['auth0']['algorithms']]

# Get config variables
user = urllib.parse.quote_plus(config['database']['db_user'])
pwd = urllib.parse.quote_plus(config['database']['db_pwd'])
db_name = config['database']['db_name']
db_host = config['database']['db_host']
db_port = config['database']['db_port']

# Set up logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
if environment == 'production':
    logger.setLevel(logging.ERROR)


# AUTHENTICATION (AUTH0)
# ===========================================

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Format error response and append status code
def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)
    
    parts = auth.split()
    
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token

def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + auth0_domain + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms = auth0_algorithms,
                    audience = auth0_audience,
                    issuer = "https://" + auth0_domain + "/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "incorrect claims,"
                                    "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 400)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 400)
    return decorated


# API ENDPOINTS
# ===========================================

@app.route('/', methods=['POST', 'DELETE', 'GET'])
@limiter.limit("1000/hour")
@cross_origin(headers=['Content-Type', 'Authorization'])
def index():
    # Get variables
    #content = request.json
    #if content is None:
    #    return make_error('JSON body not sent', 400)
    #if 'tree_id' not in content:
    #    return make_error('Tree ID (tree_id) not sent (or incorrect format)', 400)
    #tree_id = int(content['tree_id'])

    return jsonify({"msg": "this is a + " + request.method})
    #try:
    #    if request.method == 'POST':
    #        return success({"msg": "hi POST"})
    #    elif request.method == 'DELETE':
    #        return success({"msg": "hi DELETE"})
    #    elif request.method == 'GET':
    #        return success({"msg": "hi GET"})
    #except KeyError as inst:
    #    if request.method == 'DELETE':
    #        return error_not_found(inst)
    #    return make_error(inst, 409)
    #except Exception as inst:
    #    return make_error(inst, 409)


@app.route("/private")
@limiter.limit("1000/hour", key_func = lambda : 'current_user.username') # TODO use ip+user combination
@cross_origin(headers=['Content-Type', 'Authorization'])
@requires_auth
def private_place():
    return jsonify({"user": _request_ctx_stack.top.current_user})
    #return success({"user": _request_ctx_stack.top.current_user, "posts": posts.count()})



# INIT
# ===========================================

def init():
    """Initialise app with global libraries (required by unit tests)"""
    #global libraryName
    #libraryName = LibraryClass()
    return


if __name__ == '__main__':
    
    if environment == 'production':
        # Run Tornado server
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8080)
        IOLoop.instance().start()

    else:
        # Run Flask server
        app.run(debug=True, host='0.0.0.0', port=8080)
