import pytest

from app import create_app, register_extensions
from config import Config
from dao.auth import AuthDao
from dao.model.user import UserSchema
from dao.movie import MovieDao
from dao.test_db.init_test_db import init_db
from dao.user import UserDao
from service.utils import hash_password, create_token, generate_salt
from setup_db import db as database



@pytest.fixture
def app():
    cfg = Config()
    cfg.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    cfg.TESTING = True
    app = create_app(cfg)
    register_extensions(app)
    with app.app_context():
        yield app


@pytest.fixture
def db(app):
    database.init_app(app)
    database.create_all()
    database.session.commit()

    yield database

    database.session.rollback()

@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        init_db(app, db)
        yield client

@pytest.fixture
def user(db):
    salt = generate_salt()
    return AuthDao(db.session).create({"email":"test@test.com", "password":hash_password("123456", salt), "salt":salt})

@pytest.fixture
def login_headers(client, user):
    tokens = create_token(UserSchema().dump(user))
    return {"Authorization":f"Bearer {tokens['access_token']}"}


# @pytest.fixture
# def movie_dao():
#     movie_dao = MovieDao(db)
#     return movie_dao

