import pytest
from app import create_app, register_extensions
from config import Config
from dao.model.user import UserSchema
from dao.test_db.init_test_db import init_db
from dao.user import UserDao
from service.utils import create_token
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
    return UserDao(db.session).get_one(1)


@pytest.fixture
def login_headers(client, user, tokens):
    return {"Authorization": f"Bearer {tokens['access_token']}"}


@pytest.fixture
def tokens(client, user):
    return create_token(UserSchema().dump(user))


@pytest.fixture
def login_headers_user_100():
    tokens = create_token(dict(id=100, email="123456"))
    return {"Authorization": f"Bearer {tokens['access_token']}"}
