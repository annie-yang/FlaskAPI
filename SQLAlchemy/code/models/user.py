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
    def __init__(self, username, password):
        # these self must match the columns to be saved in DB
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    # find user in DB by searching for their username
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
