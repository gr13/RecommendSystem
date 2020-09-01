from app.db import db


class SkincolorModel(db.Model):
    __tablename__ = 'rskincolors'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(250), default='')
    image_file = db.Column(db.String(20), default='default.jpg')

    def __init__(self, title, image_file):
        self.title = title
        self.image_file = image_file

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_file": self.image_file
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.commit()
