from dao.auth import AuthDao
from dao.favorites import FavoriteDao
from service.auth import AuthService
from service.favorites import FavoriteService
from setup_db import db
from dao.movie import MovieDao
from service.movie import MovieService

from dao.genre import GenreDao
from service.genre import GenreService

from dao.director import DirectorDao
from service.director import DirectorService

from dao.user import UserDao
from service.user import UserService

movie_dao = MovieDao(db.session)
movie_service = MovieService(movie_dao)

director_dao = DirectorDao(db.session)
director_service = DirectorService(director_dao)

genre_dao = GenreDao(db.session)
genre_service = GenreService(genre_dao)
#
user_dao = UserDao(db.session)
user_service = UserService(user_dao)

auth_dao = AuthDao(db.session)
auth_service = AuthService(auth_dao)

favorite_dao = FavoriteDao(db.session)
favorite_service = FavoriteService(favorite_dao)
