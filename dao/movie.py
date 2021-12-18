from constants import PAGINATION
from dao.model.genre import Genre
from dao.model.movie import Movie, MovieSchema

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class MovieDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        movie = self.session.query(Movie).get(mid)
        return movie

    def get_all(self, page, status):
        if status:
            if page:
                movies = self.session.query(Movie).order_by(Movie.year.desc()).limit(PAGINATION).offset(PAGINATION*(int(page)-1)).all()
            else:
                movies = self.session.query(Movie).order_by(Movie.year.desc()).all()
        elif page:
            movies = self.session.query(Movie).limit(PAGINATION).offset(PAGINATION * (int(page) - 1)).all()
        else:
            movies = self.session.query(Movie).all()
        return movies
