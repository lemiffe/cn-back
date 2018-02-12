from services.UserService import UserService
from controllers.BaseController import BaseController


class UserController(BaseController):
    
    def __init__(self, app):
        super().__init__(app)
        self.user_service = UserService()
        self.app = app

    def routes_setup(self):
        self.app.add_url_rule('/users', 'users_index', self.index, methods=['GET'])

    def index(self):
        return self.response_success({"msg": self.user_service.r})

    def get_by_id(self):
        post_count = self.user_service.get_by_id(1)
        return jsonify({"posts": post_count})
