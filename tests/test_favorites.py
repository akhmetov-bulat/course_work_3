import pytest
from dao.model.movie import Movie
from setup_db import db
from dao.favorite import FavoriteDao
from service.favorite import FavoriteService


@pytest.fixture
def favorite_dao():
    favorite_dao = FavoriteDao(db.session)
    return favorite_dao


class TestFavoriteDao:
    @pytest.fixture(autouse=True)
    def favorite_dao(self, client, favorite_dao):
        self.favorite_dao = favorite_dao

    def test_get_all(self):
        favorites1 = self.favorite_dao.get_all(1)
        favorites2 = self.favorite_dao.get_all(2)
        assert isinstance(favorites1, list)
        for movie in favorites1:
            assert isinstance(movie, Movie)
        assert favorites2 is None

    def test_add_one(self):
        response1 = self.favorite_dao.add_one(user_id=1, mid=4)
        response2 = self.favorite_dao.add_one(user_id=3, mid=4)
        assert response1 is True
        assert response2 is False

    def test_del_one(self):
        response1 = self.favorite_dao.add_one(user_id=1, mid=4)
        response2 = self.favorite_dao.add_one(user_id=3, mid=4)
        assert response1 is True
        assert response2 is False


class TestFavoriteService:
    @pytest.fixture(autouse=True)
    def favorite_service(self, client, favorite_dao):
        self.favorite_service = FavoriteService(favorite_dao=favorite_dao)

    def test_get_all(self):
        favorites1 = self.favorite_service.get_all(1)
        favorites2 = self.favorite_service.get_all(2)
        assert isinstance(favorites1, list)
        for movie in favorites1:
            assert isinstance(movie, Movie)
        assert favorites2 is None

    def test_add_one(self):
        response1 = self.favorite_service.add_one(user_id=1, mid=4)
        response2 = self.favorite_service.add_one(user_id=3, mid=4)
        assert response1 is True
        assert response2 is False

    def test_del_one(self):
        response1 = self.favorite_service.add_one(user_id=1, mid=4)
        response2 = self.favorite_service.add_one(user_id=3, mid=4)
        assert response1 is True
        assert response2 is False


class TestFavoriteView:
    @pytest.fixture(autouse=True)
    def client(self, client, login_headers, login_headers_user_100):
        self.client = client
        self.login_headers = login_headers
        self.login_headers_user_100 = login_headers_user_100

    def test_get_all(self):
        favorites1 = self.client.get("favorites/movies", headers=self.login_headers)
        favorites2 = self.client.get("favorites/movies", headers=self.login_headers_user_100)
        print("FAVOR", favorites1.json)
        assert isinstance(favorites1.json, list)
        for movie in favorites1.json:
            assert movie["id"] is not None
        assert favorites2.json == {}

    def test_post_one(self):
        favorites1 = self.client.post("favorites/movies/5", headers=self.login_headers)
        favorites2 = self.client.post("favorites/movies/5", headers=self.login_headers_user_100)
        assert favorites1.status_code == 200
        assert favorites2.status_code == 400

    def test_del_one(self):
        favorites1 = self.client.delete("favorites/movies/3", headers=self.login_headers)
        favorites2 = self.client.delete("favorites/movies/5", headers=self.login_headers_user_100)
        assert favorites1.status_code == 200
        assert favorites2.status_code == 400
