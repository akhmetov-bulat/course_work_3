from unittest.mock import MagicMock
import pytest

from dao.model.movie import Movie
from setup_db import db
from dao.movie import MovieDao
from service.movie import MovieService

@pytest.fixture
def movie_dao():
    movie_dao = MovieDao(db.session)
    film1 = Movie(**{"title": "Йеллоустоун", "description": "Владелец ранчо пытается сохранить землю своих предков.",
                     "trailer": "https://www.youtube.com/watch?v=UKei_d0cbP4", "year": 2018, "rating": 8.6,
                     "genre_id": 17, "director_id": 1, "id": 1})
    film2 = Movie(**{"title": "Омерзительная восьмерка", "description": "США после Гражданской войны. ",
                     "trailer": "https://www.youtube.com/watch?v=lmB9VWm0okU", "year": 2015, "rating": 7.8,
                     "genre_id": 4, "director_id": 2, "id": 2})
    film3 = Movie(**{"title": "Вооружен и очень опасен", "description": "События происходят в конце XIX века ...",
                     "trailer": "https://www.youtube.com/watch?v=hLA5631F-jo", "year": 1978, "rating": 6,
                     "genre_id": 17, "director_id": 3, "id": 3})
    movie_dao.get_one = MagicMock(return_value=film3)
    movie_dao.get_all = MagicMock(return_value=[film1, film2, film3])
    return movie_dao


class TestMovieService():
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
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

