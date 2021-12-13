from dao.model.director import Director


class DirectorDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, did):
        director = self.session.query(Director).get(did)
        return director

    def get_all(self):
        directors = []
        for director in self.session.query(Director).all():
            directors.append(director)
        return directors
