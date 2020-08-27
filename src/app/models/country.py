from app.db import db


class CountryModel(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(250), default="")
    hide = db.Column(db.Boolean(), default=0)

    regions = db.relationship("RegionModel", lazy="dynamic")

    def __init__(self, title):
        self.title = title

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter(title=title).first()

    @classmethod
    def get_by_id(cls, _id):
        return cls.query.filter(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
