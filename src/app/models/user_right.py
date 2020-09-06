from app.db import db


class UserRightModel(db.Model):
    __tablename__ = 'rights'

    id = db.Column(db.Integer, primary_key=True)
    user_right = db.Column(db.String(20))

    # lazy='dynamic' does not create the list of items
    # unless it is necessary
    users = db.relationship('UserModel', lazy='dynamic', back_populates="right")

    def __init__(self, user_right):
        self.user_right = user_right

    def json(self):
        return {
            'id': self.id,
            "right": self.user_right
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_right(cls, right):
        return cls.query.filter_by(user_right=right).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
