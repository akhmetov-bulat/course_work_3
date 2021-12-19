from dao.model.user import UserSchema, UserPatch, UserPassword
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
        abort(404)

    @self_only
    def patch(self, user_id):
        user_json = request.json
        if "favourite_genre" in user_json.keys():
            user_json["favorite_genre"] = user_json.pop("favourite_genre")
        try:
            if UserPatch().load(user_json):
                user_json["id"] = user_id
                if user_service.update(user_json=user_json):
                    return "updated", 200
                abort(400)
        except:
            abort(400)


@user_ns.route('/password')
class UserView(Resource):

    @self_only
    def put(self, user_id):
        user_json = request.json
        try:
            if UserPassword().load(user_json):
                user_json["id"] = user_id
                if user_service.update_password(user_json):
                    return "updated", 200
            abort(400)
        except:
            abort(400)
