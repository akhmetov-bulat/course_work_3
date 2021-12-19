
from dao.model.movie import MovieSchema
from flask_restx import Resource, Namespace
from implemented import movie_service
from flask_restx import reqparse

parser = reqparse.RequestParser()
parser.add_argument("page", type=int, location='args')
parser.add_argument("status", type=str, location='args')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
movie_ns = Namespace('movies')


@movie_ns.route('/')
class MovieView(Resource):
    @movie_ns.expect(parser)
    def get(self):
        page = parser.parse_args()["page"]
        status = parser.parse_args()["status"]
        if status:
            if status != "new":
                status = None
        movies = movie_service.get_all(page=page, status=status)
        movies_json = movies_schema.dump(movies)
        if movies:
            return movies_json, 200
        return "", 404


@movie_ns.route('/<int:mid>')
class MovieViewMid(Resource):
    def get(self, mid):
        movie = movie_service.get_one(mid)
        if movie:
            return movie_schema.dump(movie), 200
        return "not found", 404
