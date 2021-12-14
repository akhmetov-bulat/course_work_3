from dao.model.movie import Movie
from dao.model.user import User
from setup_db import db

# moviesmap = db.Table("users_movies", db.Model.metadata,
#                      db.Column("user_id", db.Integer, db.ForeignKey('users.id')),
#                      db.Column("movie_id",db.Integer, db.ForeignKey('movies.id'))
#                      )


class UserMovie(db.Model):
    __tablename__ = 'users_movies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
