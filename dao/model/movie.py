from marshmallow import fields, Schema
from dao.model.director import DirectorSchema
from dao.model.genre import GenreSchema
from setup_db import db


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    trailer = db.Column(db.String(50))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))
    director = db.relationship("Director")
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"))
    genre = db.relationship("Genre")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    director_id = fields.Int()
    genre_id = fields.Int()
    director = fields.Nested(DirectorSchema)
    genre = fields.Nested(GenreSchema)
