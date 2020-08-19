from app.db import db
from app.models.user_rights import UserRightsModel
#from app import bcrypt

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
    can_edit = db.Column(db.Boolean(), default=0)
    can_seelog = db.Column(db.Boolean(), default=0)
    can_seeusers = db.Column(db.Boolean(), default=0)
    hide = db.Column(db.Boolean(), default=0)

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
                'can_edit': self.can_edit,
                'can_seelog': self.can_seelog,
                'can_seeusers': self.can_seeusers,
                'hide': self.hide
                }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        pass

    # @classmethod
    # def create_hashed_password(cls, password):
    #     return bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def create_random_password(cls):
        return secrets.tocken_hex(8)

