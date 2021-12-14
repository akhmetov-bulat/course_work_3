from unittest.mock import MagicMock
import pytest

from dao.model.director import Director
from setup_db import db
from dao.director import DirectorDao
from service.director import DirectorService


@pytest.fixture
def director_dao():
    director_dao = DirectorDao(db.session)
    director1 = Director(id=1, name="Director_1")
    director2 = Director(id=2, name="Director_2")
    director3 = Director(id=3, name="Director_3")
    director_dao.get_one = MagicMock(return_value=director1)
    director_dao.get_all = MagicMock(return_value=[director1, director2, director3])
    return director_dao


class TestDirectorService():
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert isinstance(director, Director)
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        for item in directors:
            assert isinstance(item, Director)
        assert len(directors) > 0
