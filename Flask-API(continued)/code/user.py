import sqlite3
from flask_restful import Resource, reqparse

# interact with sqlite3
# user objects
class User:
    # store of data
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    # find user in DB by searching for their username
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # select every row in DB from only users with username
        query = "SELECT * FROM users WHERE username=?"

        # run the query
        result = cursor.execute(query, (username,))

        # fetch the results from the first row
        row = result.fetchone()

        # if there was a row, create a user object from data from that row
        # id --> row[0]
        # username -> row[1]
        # password -> row[2]
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"

        result = cursor.execute(query, (_id,))

        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

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
        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # insert users into id, username, and password
        # id always increments, so we set it as "NULL"
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return{"message": "User created sucessfully."}, 201
