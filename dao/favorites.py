from dao.model.movie import Movie, MovieSchema
from dao.model.user import User
from dao.model.user_movie import UserMovie



class FavoriteDao:
    def __init__(self, session):
        self.session = session

    def get_all(self, user_id):
        movies = self.session.query(Movie).join(UserMovie, User).filter(User.id == user_id).all()
        return movies

    def add_one(self, mid, user_id):
        user_movie = UserMovie(user_id=user_id, movie_id=mid)
        try:
            self.session.add(user_movie)
            self.session.commit()
            return True
        except:
            return False

    def del_one(self, mid, user_id):
        user_movie = UserMovie(user_id=user_id, movie_id=mid)
        try:
            user_movie = self.session.query(UserMovie).filter(UserMovie.user_id == user_id, UserMovie.movie_id == mid).first()
            self.session.delete(user_movie)
            self.session.commit()
            return True
        except:
            return False
