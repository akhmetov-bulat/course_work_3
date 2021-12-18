from dao.model.movie import Movie, MovieSchema
from dao.model.user import User



class FavoriteDao:
    def __init__(self, session):
        self.session = session

    def get_all(self, user_id):
        user = self.session.query(User).filter(User.id == user_id).one()
        return user.movies

    def add_one(self, mid, user_id):
        user = self.session.query(User).filter(User.id == user_id).one()
        movie = self.session.query(Movie).filter(Movie.id == mid).one()
        nested = self.session.begin_nested()
        try:
            user.movies.append(movie)
            self.session.commit()
            return True
        except:
            nested.rollback()
            return False

    def del_one(self, mid, user_id):
        user = self.session.query(User).filter(User.id == user_id).one()
        movie = self.session.query(Movie).filter(Movie.id == mid).one()
        nested = self.session.begin_nested()
        try:
            user.movies.remove(movie)
            self.session.commit()
            return True
        except:
            nested.rollback()
            return False