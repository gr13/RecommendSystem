from app.models.region import RegionModel
from flask_restful import Resource


class Region(Resource):
    @classmethod
    def get(cls, region_id):
        item = RegionModel.find_by_id(region_id)
        if item:
            return item.json(), 200

        return {"message": "Region is not found"}


class RegionList(Resource):
    def get(self):
        items = RegionModel.find_all()
        if items:
            return {"regions": [item.json() for item in items]}

        return {"Message": "Regions are not found."}, 404
