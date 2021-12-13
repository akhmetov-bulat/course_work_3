from dao.model.user import User, UserSchema
from flask_restx import Resource, Namespace, abort
from implemented import user_service
from flask import request
from views.helpers import self_only


user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):

    @self_only
    def get(self, user_id):
        user_json = user_service.get_one(user_id)
        if user_json:
            return user_json, 200
        return "not found", 404

    @self_only
    def patch(self, user_id):
        req_json = request.json
        name = req_json.get("name")
        surname = req_json.get("surname")
        favorite_genre = req_json.get("favourite_genre")
        user_json = {"id": user_id, }
        if name:
            user_json["name"] = name
        if surname:
            user_json["surname"] = surname
        if favorite_genre:
            user_json["favorite_genre"] = favorite_genre
        print(user_json)
        if len(user_json.keys()) == 1:
            abort(400)
        if user_service.update(user_json=user_json):
            return "updated", 200
        return 400


@user_ns.route('/password')
class UserView(Resource):

    @self_only
    def put(self, user_id):
        req_json = request.json
        print(req_json)
        password_json = {"id": user_id,
                         "password_1": req_json.get("password_1"),
                         "password_2": req_json.get("password_2")}
        if None in password_json.values():
            abort(400)
        if user_service.update_password(password_json):
            return "updated", 200
        return 400
