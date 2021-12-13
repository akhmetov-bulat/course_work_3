from dao.model.genre import Genre, GenreSchema
from flask_restx import Resource, Namespace
from implemented import genre_service
from flask import request
# from views.helpers import auth_required, admin_required

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = genre_service.get_all()
        if genres:
            return genres_schema.dump(genres), 200
        return 'not found', 404


@genre_ns.route('/<int:gid>')
class GenreViewGid(Resource):
    def get(self, gid):
        genre = genre_service.get_one(gid)
        if genre:
            return genre_schema.dump(genre), 200
        return "not found", 404
