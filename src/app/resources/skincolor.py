from app.models.skincolor import SkincolorModel
from flask_restful import Resource


class SkinColor(Resource):
    @classmethod
    def get(cls, skincolor_id):
        item = SkincolorModel.find_by_id(skincolor_id)
        if item:
            return item.json(), 200

        return {'message': "SkinColor is not found"}


class SkinColorList(Resource):
    @classmethod
    def get(cls):
        items = SkincolorModel.find_all()
        if items:
            return {"skincolors": [item.json() for item in items]}

        return {"message": "scincolors are not found"}, 404
