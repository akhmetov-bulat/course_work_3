

class DirectorService:
    def __init__(self, director_dao):
        self.director_dao = director_dao

    def get_one(self, did):
        return self.director_dao.get_one(did)

    def get_all(self):
        return self.director_dao.get_all()
