from flask import jsonify

class BaseController:
    def __init__(self, app):
        self.app = app

    def response_success(self, obj):
        response = {
            'meta': {
                'code': '200',
                'message': 'OK'
            },
            'response': obj
        }
        response = jsonify(response)
        response.status_code = 200
        return response

    def response_error(self, msg, code):
        response = {
            'meta': {
                'code': int(code),
                'message': str(msg)
            },
            'response': None
        }
        response = jsonify(response)
        response.status_code = code
        return response