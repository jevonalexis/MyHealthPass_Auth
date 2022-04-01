from app import db
from app.Models.User import User


class DBService:
    def __init__(self):
        self.db = db

    def create_db(self):
        self.db.create_all()

    def _drop_db(self):
        self.db.drop_all()

    def _truncate(self, model: db.Model):
        model.query.delete()
        self.db.session.commit()

    def insert_row(self, row: db.Model):
        try:
            self.db.session.add(row)
            self.db.session.commit()
        except Exception as e:
            raise e

    def delete_row(self, email: str):
        try:
            User.query.filter(User.email == email).delete()
            self.db.session.commit()
        except Exception as e:
            raise e

    def get_user(self, email: str):
        try:
            return User.query.filter(User.email == email).first()
        except Exception as e:
            raise e

    def lock_user(self, email: str):
        try:
            user = User.query.filter(User.email == email).first()
            user.locked = True
            self.db.session.commit()
            return user
        except Exception as e:
            raise e

    def unlock_user(self, email: str):
        try:
            user = User.query.filter(User.email == email).first()
            user.locked = False
            self.db.session.commit()
            return user
        except Exception as e:
            raise e


if __name__ == '__main__':
    dbw = DBService()
    # dbw._drop_db()
    # dbw.create_db()
    # dbw._truncate(User)
    # u1 = User(email='u1@m.com', password='P@ssw0rd2')
    # u2 = User(email='u2@m.com', password='P@ssw0rd2')
    # dbw.insert_row(u1)
    # dbw.insert_row(u2)
    print(dbw.get_user('u1@m.com'))
    print(dbw.unlock_user('u1@m.com'))
