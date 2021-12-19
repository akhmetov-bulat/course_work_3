from flask_restx import Namespace, Resource, abort
from dao.model.user import UserSchema, AuthDataCheck
from implemented import auth_service
from flask import request
from views.users import user_ns

auth_ns = Namespace('auth')
user_schema = UserSchema()


@auth_ns.route('/register')
class RegisterView(Resource):
    def post(self):
        try:
            if AuthDataCheck().load(request.json):
                user_json = auth_service.create(request.json)
                if user_json:
                    return user_json, 201, {'Location': f"/{user_ns}/{user_json['id']}"}
                abort(400)
        except:
            abort(400)


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        if AuthDataCheck().load(request.json):
            data = auth_service.auth_get_token(request.json)
            if not data:
                abort(401, error="Неверные учётные данные")
            return data, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if not refresh_token:
            abort(400)
        data = auth_service.auth_refresh_token(refresh_token)
        if not data:
            abort(401, error="Неверные учётные данные")
        return data, 201
