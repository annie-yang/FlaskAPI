import sqlite3
from db import db

# interact with sqlite3
# user objects
# 'db.Model' creates a mapping to the DB
class UserModel(db.Model):
    # where to insert the table
    __tablename__ = 'users'

    # columns the model will have (id, username, passord)
    # telling the DB that there is id that contains integer and primary_key (unique)
    id = db.Column(db.Integer, primary_key=True)
    # '(80)' limits size of username and password
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # store of data
    def __init__(self, _id, username, password):
        # these self must match the columns to be saved in DB
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
