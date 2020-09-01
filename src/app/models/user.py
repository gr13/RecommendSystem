from app.db import db
from app.models.user_rights import UserRightsModel
#from app import bcrypt
from sqlalchemy.orm import validates

import secrets


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(60))
    right_id = db.Column(
        db.Integer,
        db.ForeignKey('rights.id'),
        default=1
    )
    right = db.relationship('UserRightsModel')

    username = db.Column(db.String(100), default='')
    position = db.Column(db.String(100), default='')
    hide = db.Column(db.Boolean(), default=0)

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def json(self):
        right = UserRightsModel.find_by_id(self.right_id)
        return {'id': self.id,
                'email': self.email,
                'right_id': self.right_id,
                'right': right.json(),
                'username': self.username,
                'position': self.position,
                'hide': self.hide
                }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def create_hashed_password(cls, password):
    #     return bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def create_random_password(cls):
        return secrets.tocken_hex(8)

