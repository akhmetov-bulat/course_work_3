from setup_db import db


class UserMovie(db.Model):
    __tablename__ = 'users_movies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    user = db.relationship("User")
    movie_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie = db.relationship("Movie")
