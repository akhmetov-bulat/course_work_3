import pytest
from dao.model.genre import Genre
from setup_db import db
from dao.genre import GenreDao
from service.genre import GenreService


@pytest.fixture
def genre_dao():
    genre_dao = GenreDao(db.session)
    return genre_dao


class TestGenreDao:
    @pytest.fixture(autouse=True)
    def genre_dao(self, client, genre_dao):
        self.genre_dao = genre_dao

    def test_get_one(self, gid=2):
        genre = self.genre_dao.get_one(gid)
        assert genre.id == 2
        assert isinstance(genre, Genre)

    def test_get_all(self):
        genres = self.genre_dao.get_all()
        assert isinstance(genres, list)
        for item in genres:
            assert isinstance(item, Genre)
        assert len(genres) > 0


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, client, genre_dao):
        self.genre_service = GenreService(genre_dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert isinstance(genre, Genre)
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert isinstance(genres, list)
        for item in genres:
            assert isinstance(item, Genre)
        assert len(genres) > 0


class TestGenreView:
    @pytest.fixture(autouse=True)
    def client(self, client):
        self.client = client

    def test_get_all(self):
        response = self.client.get("/genres/")
        assert isinstance(response.json, list)
        assert len(response.json) > 3
        assert response.status_code == 200

    def test_get_one(self):
        response = self.client.get("/genres/2")
        assert isinstance(response.json, dict)
        assert response.json["id"] == 2
        assert response.status_code == 200

    def test_get_one_fail(self):
        response = self.client.get("/genres/222")
        assert response.status_code == 404
