from dao.model.movie import Movie
from dao.model.user import User


class FavoriteDao:
    def __init__(self, session):
        self.session = session

    def get_all(self, user_id):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user:
            if user.movies:
                return user.movies
        return None

    def add_one(self, mid, user_id):
        user = self.session.query(User).filter(User.id == user_id).first()
        movie = self.session.query(Movie).filter(Movie.id == mid).first()
        nested = self.session.begin_nested()
        try:
            user.movies.append(movie)
            self.session.commit()
            return True
        except:
            nested.rollback()
        return False

    def del_one(self, mid, user_id):
        user = self.session.query(User).filter(User.id == user_id).first()
        movie = self.session.query(Movie).filter(Movie.id == mid).first()
        nested = self.session.begin_nested()
        try:
            user.movies.remove(movie)
            self.session.commit()
            return True
        except:
            nested.rollback()
            return False
