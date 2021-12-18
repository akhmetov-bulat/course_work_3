from service.utils import hash_password, create_token, compare_password, generate_salt
from dao.model.user import User, UserSchema
import jwt
from constants import SECRET, algo

user_schema = UserSchema()

class AuthService:
    def __init__(self, auth_dao):
        self.auth_dao = auth_dao

    def create(self, user_json):
        new_salt = generate_salt()
        hashed_password = hash_password(user_json["password"], new_salt)
        user_json["salt"] = new_salt
        user_json["password"] = hashed_password
        new_user = self.auth_dao.create(user_json)
        if new_user:
            return user_schema.dump(new_user)
        return None

    def auth_get_token(self, req_json):
        user = self.auth_dao.get_by_email(req_json["email"])
        if user is None:
            return None
        if compare_password(req_json["password"], user.password, user.salt):
            data = {"id":user.id,
                    "email": user.email,
                    "role": user.role
                    }
            tokens = create_token(data)
            return tokens
        return None

    def auth_refresh_token(self, refresh_token):
        try:
            token_data = jwt.decode(jwt=refresh_token, key=SECRET, algorithms=[algo])
        except:
            return None
        email = token_data.get('email')
        user = self.auth_dao.get_by_email(email)
        if user is None:
            return None
        data = {"id":user.id,
                "email": user.email,
                "role": user.role
                }
        tokens = create_token(data)
        return tokens
