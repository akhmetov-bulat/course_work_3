from marshmallow import Schema

from setup_db import db

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
