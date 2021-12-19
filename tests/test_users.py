import pytest
from setup_db import db
from dao.model.user import User
from dao.user import UserDao
from service.user import UserService


@pytest.fixture
def user_dao():
    user_dao = UserDao(db.session)
    return user_dao


@pytest.fixture
def user_patch_json():
    return {"name": "123456", "surname": "123456", "favorite_genre": "1"}


@pytest.fixture
def user_patch_json_fail():
    return {"name": "", "surname": "", "favorite_genre": ""}


@pytest.fixture
def user_put_json():
    return {"password_1": "123456", "password_2": "654321"}


class TestUserDao:
    @pytest.fixture(autouse=True)
    def user_dao(self, client, user_dao):
        self.user_dao = user_dao

    def test_check_email(self):
        response1 = self.user_dao.check_email("asdf")
        response2 = self.user_dao.check_email("asdfasdf")
        assert response1 is True
        assert response2 is False

    def test_get_by_email(self):
        response1 = self.user_dao.get_by_email("asdf")
        response2 = self.user_dao.get_by_email("asdfasdf")
        assert isinstance(response1, User)
        assert response1.id == 1
        assert response2 is None

    def test_get_one(self):
        response1 = self.user_dao.get_one(1)
        response2 = self.user_dao.get_one(10)
        assert isinstance(response1, User)
        assert response1.id == 1
        assert response2 is None

    def test_update(self):
        user_json = {"id": 1, "name": "undefined"}
        response1 = self.user_dao.update(user_json)
        response2 = self.user_dao.update("user_json")
        assert response1 is True
        assert response2 is False


class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self, client, user_dao):
        self.user_service = UserService(user_dao=user_dao)

    def test_get_one(self):
        user = self.user_service.get_one(1)
        assert user["id"] == 1

    def test_update(self):
        update_json = {"id": 1,
                       "name": "456"}
        assert self.user_service.update(update_json) is True

    def test_update_password(self):
        update_json = {"id": 1,
                       "password_1": "123456",
                       "password_2": "456"}
        assert self.user_service.update_password(password_json=update_json) is True


class TestUserView:
    @pytest.fixture(autouse=True)
    def client(self, client, login_headers, login_headers_user_100):
        self.client = client
        self.login_headers = login_headers
        self.login_headers_user_100 = login_headers_user_100

    def test_user_get_self(self):
        response1 = self.client.get("/user/", headers=self.login_headers)
        response2 = self.client.get("/user/", headers=self.login_headers_user_100)
        assert response1.json['id'] == 1
        assert response1.status_code == 200
        assert response2.status_code == 404

    def test_user_patch_self(self, user_patch_json, user_patch_json_fail):
        response1 = self.client.patch("/user/", headers=self.login_headers, json=user_patch_json)
        response2 = self.client.patch("/user/", headers=self.login_headers, json=user_patch_json_fail)
        assert response1.json == "updated"
        assert response1.status_code == 200
        assert response2.status_code == 400

    def test_user_put_self(self, user_put_json):
        response1 = self.client.put("/user/password", headers=self.login_headers, json=user_put_json)
        response2 = self.client.put("/user/password", headers=self.login_headers, json=user_put_json)
        assert response1.json == "updated"
        assert response1.status_code == 200
        assert response2.status_code == 400
