from dao.model.director import DirectorSchema
from flask_restx import Resource, Namespace
from implemented import director_service


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = director_service.get_all()
        if directors:
            return directors_schema.dump(directors), 200
        return 'not found', 404


@director_ns.route('/<int:did>')
class DirectorViewDid(Resource):

    def get(self, did):
        director = director_service.get_one(did)
        if director:
            return director_schema.dump(director), 200
        return "not found", 404
