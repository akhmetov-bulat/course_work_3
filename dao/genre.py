from dao.model.genre import Genre


class GenreDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        genre = self.session.query(Genre).get(gid)
        return genre

    def get_all(self):
        genres = []
        for genre in self.session.query(Genre).all():
            genres.append(genre)
        return genres
