from dao.model.user import User


class UserDao:
    def __init__(self, session):
        self.session = session

    def check_email(self, email):
        if self.session.query(User).filter(User.email == email).first():
            return True
        return False

    def get_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        if user:
            return user
        return None

    def get_one(self, uid):
        user = self.session.query(User).get(uid)
        if user:
            return user
        return None

    def update(self, user_json):
        # try:
        self.session.query(User).filter(User.id == user_json.get("id")).update(user_json)
        self.session.commit()
        return True
        # except:
        #     return False

    def update_password(self, user):
        try:
            self.session.update(user)
            self.session.commit()
            return True
        except:
            return False

