from pymongo import MongoClient

class UserService:

    def __init__(self):
        self.r = 2

    def get_by_id(self, id):
        #client = MongoClient(db_host, int(db_port), username=user, password=pwd)
        #db = client[db_name]
        #posts = db.posts
        #post_count = posts.count()
        #return post_count
        return 1