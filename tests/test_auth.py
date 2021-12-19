import pytest
from dao.model.user import User
from setup_db import db
from dao.auth import AuthDao
from service.auth import AuthService


@pytest.fixture
def auth_dao():
    auth_dao = AuthDao(db.session)
    return auth_dao


@pytest.fixture
def reg_json():
    return dict(email="test_email", password="123456")


class TestAuthView:
    @pytest.fixture(autouse=True)
    def client(self, client, login_headers, login_headers_user_100):
        self.client = client
        self.login_headers = login_headers
        self.login_headers_auth_100 = login_headers_user_100

    def test_auth_register_post(self, reg_json):
        self.reg_json = reg_json
        response1 = self.client.post("/auth/register", json=self.reg_json)
        response2 = self.client.post("/auth/register", json={"email": "email"})
        response3 = self.client.post("/auth/register", json={"email": "asdf", "password": "123456"})
        assert response1.json['id'] == 3
        assert response1.status_code == 201
        assert response2.status_code == 400
        assert response3.status_code == 400

    def test_auth_login_post(self, reg_json):
        self.reg_json = reg_json
        self.client.post("/auth/register", json=self.reg_json)
        response1 = self.client.post("/auth/login", json=self.reg_json)
        response2 = self.client.post("/auth/login", json={"email": "email", "password": "password"})
        print("response1.json", response1.json)
        assert response1.json['access_token']
        assert response1.status_code == 201
        assert response2.status_code == 401

    def test_auth_login_put(self, tokens):
        self.tokens = tokens
        response1 = self.client.put("/auth/login", json=self.tokens)
        response2 = self.client.put("/auth/login", json={"refresh_token": ""})
        response3 = self.client.put("/auth/login", json={"refresh_token": "asdfasdf"})
        assert response1.json['access_token']
        assert response1.status_code == 201
        assert response2.status_code == 400
        assert response3.status_code == 401
