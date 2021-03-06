import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # 'precision(2) moves decimal two spaces'
    price = db.Column(db.Float(precision=2))

    # determine which 'store' it belongs to
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    # sees we have a store id and can find the store id
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # dictionary
    def json(self):
        return {
            'name': self.name,
            'price': self.price
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
