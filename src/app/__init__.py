from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
# from flask_bcrypt import Bcrypt
from app.blacklist import BLACKLIST

from app.resources.user import (
    UserRegister,
    User,
    UserLogin,
    UserLogout,
    UserList
)

from app.resources.skincolor import SkinColor, SkinColorList

from app.resources.country import CountryList, Country
from app.resources.region import RegionList, Region

from app.models.user import UserModel

#  remove as soon as SQL is ready
from app.models.user_rights import UserRightsModel
from app.models.country import CountryModel

from app.db import db

import os
import sys

# flask logger
sys.stdout = sys.stderr = open('log/flasklog.txt', 'w+')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret'  # os.environ['FLASK_SECRET_KEY']
app.config['DEBUG'] = True  # os.environ['DEBUG']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api = Api(app)
# bcrypt = Bcrypt(app)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()

    if len([item for item in UserRightsModel.find_all()]) == 0:
        # we need to create Rights only once!
        right = UserRightsModel('blocked')
        right.save_to_db()
        right = UserRightsModel('customer')
        right.save_to_db()
        right = UserRightsModel('operator')
        right.save_to_db()
        right = UserRightsModel('chief operator')
        right.save_to_db()
        right = UserRightsModel('manager')
        right.save_to_db()
        right = UserRightsModel('regional manager')
        right.save_to_db()
        right = UserRightsModel('admin')
        right.save_to_db()

    if len([item for item in CountryModel.find_all()]) == 0:
        country = CountryModel("USA")
        country.save_to_db()
        country = CountryModel("Germany")
        country.save_to_db()
        country = CountryModel("Finland")
        country.save_to_db()
        country = CountryModel("UK")
        country.save_to_db()
    if len([item for item in UserModel.find_all()]) == 0:
        user = UserModel("admin@admin.com", "test")
        user.right_id = 7
        user.save_to_db()
        user = UserModel("oper@oper.com", "test")
        user.right_id = 3
        user.save_to_db()
        user = UserModel("customer@customer.com", "test")
        user.right_id = 2
        user.save_to_db()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    rights = {
        "right_id": 1,
        "is_admin": 0,
        "is_blocked": 1
    }
    if user:
        rights = {
            "right_id": user.right_id,
            "is_admin": user.right_id == 7,
            "is_blocked": user.right_id == 1
        }

    return rights


api.add_resource(Country, '/country/<string:title>')
api.add_resource(CountryList, '/countries')

api.add_resource(Region, '/region/<int:region_id>')
api.add_resource(RegionList, '/regions')

api.add_resource(SkinColor, '/skincolor/<int:skincolor_id>')
api.add_resource(SkinColorList, "/skincolors")


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserList, '/users')


@app.route("/")
def hello():
    return "Hello World!"
