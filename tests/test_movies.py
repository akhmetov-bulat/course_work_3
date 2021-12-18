import pytest
from setup_db import db
from dao.model.movie import Movie
from dao.movie import MovieDao
from contextlib import contextmanager

from service.movie import MovieService

@pytest.fixture
def movie_dao():
    movie_dao = MovieDao(db.session)
    return movie_dao


@contextmanager
def does_not_raise():
    yield

@contextmanager
def not_raise():
    yield


args_get_all = [[8,"new", None, None, 0, pytest.raises(IndexError)],
        [None,None, 1, 2018, 20, does_not_raise()],
        [1,None, 1, 2018, 3, does_not_raise()],
        [None,"new", 12, 2021, 20, does_not_raise()],
        ["1","new", 12, 2021, 3, does_not_raise()],
        [7,"new", 15, 1980, 2, does_not_raise()],
        [8,"new", None, None, 0, pytest.raises(IndexError)]]

args_get_all_view = [[8,"new", None, None, 0, pytest.raises(IndexError)],
        [None,None, 1, 2018, 20, does_not_raise()],
        [1,None, 1, 2018, 3, does_not_raise()],
        [None,"new", 12, 2021, 20, does_not_raise()],
        ["1","new", 12, 2021, 3, does_not_raise()],
        [7,"new", 15, 1980, 2, does_not_raise()],
        [8,"new", None, None, 0, pytest.raises(IndexError)]]


args_get_one = [[1, 200, does_not_raise()],
                [2, 200, does_not_raise()],
                [3, 200,  does_not_raise()],
                [111, 404, pytest.raises(AttributeError)]]


class TestMovieDao():
    @pytest.fixture(autouse=True)
    def movie_dao(self, client, movie_dao):
        self.movie_dao = movie_dao

    def test_get_one(self, mid=2):
        movie = self.movie_dao.get_one(mid)
        assert movie.id == 2
        assert isinstance(movie, Movie)

    @pytest.mark.parametrize('page, status, exp_id, exp_year, exp_len, expectation', args_get_all)
    def test_get_all(self, page, status, exp_id, exp_year, exp_len, expectation):
        with expectation:
            movies = self.movie_dao.get_all(page=page, status=status)
            for item in movies:
                assert isinstance(item, Movie)
            assert movies[0].id == exp_id
            assert movies[0].year == exp_year
            assert len(movies) == exp_len


class TestMovieService():
    @pytest.fixture(autouse=True)
    def movie_service(self, client, movie_dao):
        self.movie_service = MovieService(movie_dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(3)
        assert isinstance(movie, Movie)
        assert movie.id == 3

    def test_get_all(self):
        movies = self.movie_service.get_all(page=None, status=None)
        for item in movies:
            assert isinstance(item, Movie)
        assert len(movies)>0


class TestMovieView:
    @pytest.fixture(autouse=True)
    def client(self, client):
        self.client = client

    def test_get_all(self):
        response = self.client.get("/movies/")
        assert len(response.json) > 3
        assert response.status_code == 200

    @pytest.mark.parametrize('page, status, exp_id, exp_year, exp_len, expectation', args_get_all_view)
    def test_get_all_params(self,page, status, exp_id, exp_year, exp_len, expectation):
        with expectation:
            status_ = ("status=" + status) if status else ""
            page_ = ("page=" + str(page)) if page else""
            if_both = "&" if page and status else ""
            response = self.client.get(f"/movies/?{status_}{if_both}{page_}")
            assert len(response.json) == exp_len
            assert response.json[0]["id"] == exp_id
            assert response.status_code == 200

    @pytest.mark.parametrize("mid, stat, expectation", args_get_one)
    def test_get_one(self, mid, stat, expectation):
        with expectation:
            response = self.client.get(f"/movies/{mid}")
            assert response.json.get("id") == mid
            assert response.status_code == stat
