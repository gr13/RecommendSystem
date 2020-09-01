from app.db import db


class RegionModel(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255), default="")
    country_id = db.Column(
        db.Integer,
        db.ForeignKey("countries.id"),
        default=1
    )
    country = db.relationship("CountryModel")

    def __init__(self, title, country_id):
        self.title = title
        self.country_id = country_id

    def json(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "country_id": self.country_id}

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

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
