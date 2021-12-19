from flask_restx import Namespace, Resource, abort

from dao.model.movie import MovieSchema
from implemented import favorite_service
from views.helpers import self_only

favorites_movies_ns = Namespace('favorites/movies')
movies_schema = MovieSchema(many=True)


@favorites_movies_ns.route('/')
class FavoriteView(Resource):
    @self_only
    def get(self, user_id):
        movies = favorite_service.get_all(user_id=user_id)
        return movies_schema.dump(movies), 200


@favorites_movies_ns.route('/<int:mid>')
class FavoriteView(Resource):
    @self_only
    def post(self, mid: int, user_id):
        if favorite_service.add_one(mid=mid, user_id=user_id):
            return "", 200
        abort(400)

    @self_only
    def delete(self, mid: int, user_id):
        if favorite_service.del_one(mid=mid, user_id=user_id):
            return "", 200
        abort(400)
