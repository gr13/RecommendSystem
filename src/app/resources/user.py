from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from app.blacklist import BLACKLIST
from app.models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
    get_jwt_claims
)

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'email',
    type=str,
    required=True,
    help="This field cannot be blanc."
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help="This field cannot be blank."
)


class UserRegister(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Only admin can register a user."}, 400
        data = _user_parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {'message': 'A user with that username already exists.'}, 400

        # TODO fix the problem with circular input
        # hashed_password = UserModel.create_hashed_password(data['password'])
        hashed_password = data['password']
        user = UserModel(data['email'], hashed_password)
        user.save_to_db()

        return {"message": "User created successfully."}


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be empty")
    parser.add_argument('password',
                        type=str,
                        required=False)
    parser.add_argument('right_id',
                        type=int,
                        required=False)
    parser.add_argument('username',
                        type=str,
                        required=False,
                        help="This field cannot be empty")
    parser.add_argument('position',
                        type=str,
                        required=False)

    parser.add_argument('hide',
                        type=1,
                        choices=[0, 1],
                        required=False,
                        help="This field accepts only 0 and 1")

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 200
        return {'message': "User not found"}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}, 200

        return {"message": "User not found"}, 404

    @classmethod
    def put(cls, user_id):
        data = User.parser.parse_args()

        item = UserModel.find_by_id(user_id)

        if not item:
            if data["password"]:
                item = UserModel(data["email"], data["password"])
            else:
                return {"message": "User creation requires password."}

        if data['password'] is not None:
            item.password = data['password']
        if data['right_id'] is not None:
            item.right_id = data['right_id']
        if data['username'] is not None:
            item.username = data['username']
        if data['hide'] is not None:
            item.hide = data['hide']
        item.save_to_db()

        return item.json()



class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200


class UserList(Resource):
    def get(self):
        items = UserModel.find_all()
        if items:
            return {"users": [item.json() for item in items]}, 200
        return {"message": "Users not found."}, 404
