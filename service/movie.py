
class MovieService:
    def __init__(self, movie_dao):
        self.movie_dao = movie_dao

    def get_one(self, mid):
        return self.movie_dao.get_one(mid)

    def get_all(self,page, status):
        return self.movie_dao.get_all(page, status)
