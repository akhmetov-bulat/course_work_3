import pytest
from dao.model.director import Director
from setup_db import db
from dao.director import DirectorDao
from service.director import DirectorService


@pytest.fixture
def director_dao():
    director_dao = DirectorDao(db.session)
    return director_dao


class TestDirectorDao:
    @pytest.fixture(autouse=True)
    def director_dao(self, client, director_dao):
        self.director_dao = director_dao

    def test_get_one(self, gid=2):
        director = self.director_dao.get_one(gid)
        assert director.id == 2
        assert isinstance(director, Director)

    def test_get_all(self):
        directors = self.director_dao.get_all()
        assert isinstance(directors, list)
        for item in directors:
            assert isinstance(item, Director)
        assert len(directors) > 0


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, client, director_dao):
        self.director_service = DirectorService(director_dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert isinstance(director, Director)
        assert director.id == 1

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert isinstance(directors, list)
        for item in directors:
            assert isinstance(item, Director)
        assert len(directors) > 0


class TestDirectorView:
    @pytest.fixture(autouse=True)
    def client(self, client):
        self.client = client

    def test_get_all(self):
        response = self.client.get("/directors/")
        assert isinstance(response.json, list)
        assert len(response.json) > 3
        assert response.status_code == 200

    def test_get_one(self):
        response = self.client.get("/directors/2")
        assert isinstance(response.json, dict)
        assert response.json["id"] == 2
        assert response.status_code == 200

    def test_get_one_fail(self):
        response = self.client.get("/directors/222")
        assert response.status_code == 404

    def test_get_all_fail(self):
        nested = db.session.begin_nested()
        try:
            db.session.drop_all()
            response = self.client.get("/directors/222")
            assert response.status_code == 404
        except:
            nested.rollback()
