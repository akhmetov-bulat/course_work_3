from flask import Flask
from config import Config
from setup_db import db
from flask_restx import Api

from views.favorites import favorites_movies_ns
from views.movies import movie_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.users import user_ns
from views.auth import auth_ns
from dao.test_db.init_test_db import init_db
from flask_cors import CORS



def create_app(cfg):
    app = Flask(__name__)
    cors = CORS()
    app.url_map.strict_slashes = False
    app.config.from_object(cfg)
    cors.init_app(app)
    db.init_app(app)

    return app


def register_extensions(app):
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(favorites_movies_ns)
    init_db(app, db)


cfg = Config()
app = create_app(cfg)

register_extensions(app)


if __name__ == '__main__':
    app.run()