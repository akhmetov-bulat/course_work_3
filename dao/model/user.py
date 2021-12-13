from constants import PWD_HASH_SALT
from dao.model.genre import GenreSchema, Genre
from setup_db import db
from marshmallow import Schema, fields


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    salt = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user", nullable=False)
    favorite_genre = db.Column(db.Integer, db.ForeignKey("genres.id"), default=1)
    genre = db.relationship("Genre")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str()
    password = fields.Str(load_only=True)
    name = fields.Str()
    surname = fields.Str()
    salt = fields.Str(load_only=True)
    role = fields.Str(load_only=True)
    genre = fields.Nested(GenreSchema)
