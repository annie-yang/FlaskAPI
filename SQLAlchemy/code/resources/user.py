import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    # post some data to user register
    def post(self):
        # expect username and password from 'parser.add_argument'
        data = UserRegister.parser.parse_args()

        # if username already exists, send a message that it exists
        # if username with that data is not none, then that username already exists
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        # for each of keys in data, pass all username and password
        user = UserModel(**data)
        user.save_to_db()

        return{"message": "User created sucessfully."}, 201
