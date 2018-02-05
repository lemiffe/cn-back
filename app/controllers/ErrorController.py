from controllers.BaseController import BaseController
from flask import jsonify

class ErrorController(BaseController):
    
    def __init__(self, app):
        super().__init__(app)
        self.app.register_error_handler(404, self.error_not_found)
        self.app.register_error_handler(500, self.error_unknown)

    def error_not_found(self, error=None):
        output_error = 'Resource not found.'
        if error is not None:
            if isinstance(error, str):
                output_error = error
            else:
                try:
                    output_error += ' ' + str(error.description)
                except Exception as inst:
                    output_error += ' ' + str(inst)
        return self.response_error(output_error, 404)


    def error_unknown(self, error=None):
        output_error = 'Internal server error. We have caught this and we have been notified.'
        # TODO: If on production environment don't do the following
        if error is not None:
            if isinstance(error, str):
                output_error = error
            else:
                try:
                    output_error += ' ' + str(error.description)
                except Exception as inst:
                    output_error += ' ' + str(inst)
        return self.response_error(output_error, 500)
