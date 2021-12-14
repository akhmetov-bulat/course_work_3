import json

from dao.model.director import Director
from dao.model.genre import Genre
from dao.model.movie import Movie
from dao.model.user import User
from dao.model.user_movie import UserMovie
from service.utils import generate_salt, hash_password


def check_database():
    from constants import DB_FILENAME
    if DB_FILENAME == ":memory:":
        return False
    from os.path import isfile
    if not isfile(DB_FILENAME):
        return False
    return True


def init_db(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()
        with db.session.begin():
            entities = []
            with open('./dao/test_db/test_db.json', 'r', encoding='UTF-8') as f:
                raw_json = json.load(f)
                movies = raw_json["movies"]
                genres = raw_json["genres"]
                directors = raw_json["directors"]
                for item in movies:
                    item["id"] = item.pop("pk")
                    entities.append(Movie(**item))
                for item in genres:
                    item["id"] = item.pop("pk")
                    entities.append(Genre(**item))
                for item in directors:
                    item["id"] = item.pop("pk")
                    entities.append(Director(**item))
            u1_salt = generate_salt()
            u1_raw_password = "123456"
            u1_password = hash_password(u1_raw_password, u1_salt)
            item1 = {"email":"asdf", "password":u1_password, "role":"admin", "name":"name", "surname":"surname", "salt":u1_salt}
            entities.append(User(**item1))
            u2_salt = generate_salt()
            u2_raw_password = "123456"
            u2_password = hash_password(u2_raw_password, u2_salt)
            item2 = {"email": "qwer", "password": u2_password, "role": "user", "name": "name", "surname": "surname", "salt": u2_salt}
            user_movie1 = {"user_id": 1, "movie_id": 1}
            user_movie2 = {"user_id": 1, "movie_id": 2}
            user_movie3 = {"user_id": 1, "movie_id": 3}

            entities.append(UserMovie(**user_movie1))
            entities.append(UserMovie(**user_movie2))
            entities.append(UserMovie(**user_movie3))
            entities.append(User(**item2))
            db.session.add_all(entities)

