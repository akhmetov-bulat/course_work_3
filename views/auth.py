from flask_restx import Namespace, Resource, abort
from dao.model.user import UserSchema
from implemented import auth_service
from flask import request

from views.users import user_ns

auth_ns = Namespace('auth')
user_schema = UserSchema()


@auth_ns.route('/register')
class RegisterView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email', None)
        password = req_json.get('password', None)
        name = req_json.get('name', "unnamed")
        surname = req_json.get('surname', "unnamed")
        print(email, password)
        if None in [email, password]:
            abort(400)
        user_json = auth_service.create(email=email, new_password=password, name=name, surname=surname)
        if user_json:
            return user_json, 201, {'Location': f"/{user_ns}/{user_json['id']}"}
        abort(401)

@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email', None)
        password = req_json.get('password', None)
        if None in [email, password]:
            abort(400)
        data = auth_service.auth_get_token(email, password)
        if not data:
            abort(401, error="Неверные учётные данные")
        return data, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)
        data = auth_service.auth_refresh_token(refresh_token)
        if not data:
            abort(401, error="Неверные учётные данные")
        return data, 201
