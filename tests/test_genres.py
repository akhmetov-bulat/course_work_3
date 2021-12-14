from unittest.mock import MagicMock
import pytest

from dao.model.genre import Genre
from setup_db import db
from dao.genre import GenreDao
from service.genre import GenreService


@pytest.fixture
def genre_dao():
    genre_dao = GenreDao(db.session)
    genre1 = Genre(id=1, name="Genre_1")
    genre2 = Genre(id=2, name="Genre_2")
    genre3 = Genre(id=3, name="Genre_3")
    genre_dao.get_one = MagicMock(return_value=genre1)
    genre_dao.get_all = MagicMock(return_value=[genre1, genre2, genre3])
    return genre_dao


class TestGenreService():
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(genre_dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert isinstance(genre, Genre)
        assert genre.id == 1

    def test_get_all(self):
        genres = self.genre_service.get_all()
        for item in genres:
            assert isinstance(item, Genre)
        assert len(genres) > 0

