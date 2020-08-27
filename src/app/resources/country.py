from app.models.country import CountryModel
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity)


class Country(Resource):
    @classmethod
    def get(cls, title):
        item = CountryModel.find_by_title(title)
        if item:
            return item.json(), 200

        return {"message": "Country is not found"}

    @classmethod
    @jwt_required
    def post(cls, title):
        user_id = get_jwt_identity()

        item = CountryModel(title)

        try:
            item.save_to_db()
        except:
            return {"message", "An error occurred inserting new country"}

        return item.json(), 201



    @classmethod
    def delete(cls, title):
        pass

    @classmethod
    def put(cls):
        pass


class CountryList(Resource):
    def get(self):
        items = [item.json() for item in CountryModel.find_all()]
        if items:
            return {"countries": items}, 200
        return {"message": "Countries not found"}, 404
