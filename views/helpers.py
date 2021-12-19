import jwt
from flask import abort, request
from constants import SECRET, algo


def self_only(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)
        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        decoded_data = {}
        try:
            decoded_data = jwt.decode(token, SECRET, algorithms=[algo])
        except:
            abort(401)
        return func(*args, **kwargs, user_id=decoded_data["id"])  # если убрать в блок try - тесты не проходят
    return wrapper
