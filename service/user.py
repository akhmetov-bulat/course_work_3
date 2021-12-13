from dao.model.user import UserSchema
from service.utils import generate_salt, hash_password, compare_password

user_schema = UserSchema()

class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def get_one(self, uid):
        user = self.user_dao.get_one(uid)
        user_json = user_schema.dump(user)
        return user_json

    def update(self, user_json):
        return self.user_dao.update(user_json=user_json)

    def update_password(self, password_json):
        user_id = password_json.get("id")
        old_password = password_json.get("password_1")
        user = self.user_dao.get_one(user_id)
        if compare_password(old_password, user.password, user.salt):

            new_password = password_json.get("password_2")
            new_hashed_password = hash_password(new_password, user.salt)
            update_json = {"id": user_id,
                           "password": new_hashed_password}
            return self.user_dao.update(update_json)
        return None
