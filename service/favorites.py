

class FavoriteService:
    def __init__(self, favorite_dao):
        self.favorite_dao = favorite_dao

    def add_one(self, mid, user_id):
        return self.favorite_dao.add_one(mid=mid, user_id=user_id)

    def get_all(self, user_id):
        return self.favorite_dao.get_all(user_id=user_id)

    def del_one(self, mid, user_id):
        return self.favorite_dao.del_one(mid=mid, user_id=user_id)
