from dao.model.user import User


class AuthDao:
    def __init__(self, session):
        self.session = session

    def check_email(self, email):
        if self.session.query(User).filter(User.email == email).first():
            return True
        return False

    def create(self, user_json):
        try:
            new_user = User(**user_json)
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except:
            return None

    def get_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        if user:
            return user
        return None
