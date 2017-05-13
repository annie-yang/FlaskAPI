import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    # dictionary
    def json(self):
        return {
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

    # class method because it's returning an object instead of a dictionary
    @classmethod
    def find_by_name(cls, name):
        # select all items where name = name LIMIT 1 -- return the first row only
        return cls.query.filter_by(name=name).first()

    # saving the model to DB
    def save_to_db(self):
        # insert 'this' object to DB
        # 'session' are collection of objects we write to DB
        db.session.add(self)
        db.session.commit()

    # delete from DB
    def delete_from_db(self):
            db.session.delete(self)
            db.session.commit()
