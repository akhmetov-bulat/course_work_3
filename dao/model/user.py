from constants import PWD_HASH_SALT
from dao.model.genre import GenreSchema, Genre
from setup_db import db
from marshmallow import Schema, fields

favorite = db.Table("favorites",
                    db.Column("user_id", db.Integer, db.ForeignKey('users.id'), primary_key=True),
                    db.Column("movie_id",db.Integer, db.ForeignKey('movies.id'), primary_key=True)
                    )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(30))
    salt = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user", nullable=False)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genres.id"), default=1)
    genre = db.relationship("Genre")
    movies = db.relationship("Movie", secondary="favorites", lazy="subquery",
                             backref=db.backref("movies", lazy=True))

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    password = fields.Str(load_only=True)
    name = fields.Str()
    surname = fields.Str()
    salt = fields.Str(load_only=True)
    role = fields.Str(load_only=True)
    favorite_genre = fields.Int()
    genre = fields.Nested(GenreSchema)


class AuthDataCheck(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class UserPatch(Schema):
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Int()

class UserPassword(Schema):
    password_1 = fields.Str(required=True)
    password_2 = fields.Str(required=True)
