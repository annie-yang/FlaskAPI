# CRUD
# Create -- post
# Read -- get
# Update -- put
# Delete -- delete

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# one resource
# retrieving resources from student class
class Item(Resource):
    # parser belongs to class itself
    parser = reqparse.RequestParser()

    # passing only certain fields to our endpoint
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    # retrieve items from the DB
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item
        return {"message": "Item not found"}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        # if row exists, then return the name and price
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    # creating items
    def post(self,name):
        # return item if it already exists (from function "find_by_name")
        # make sure item is not already in the DB
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)},400 # something went wrong with request

        # parses data
        data = Item.parser.parse_args()

        # JSON data
        item = {
            'name': name,
            'price': data['price']
        }

        # exception block
        try:
            self.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error

        # return the item to DB
        # HTTP status code '201' means object has been created
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"

        # insert JSON data into DB
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # delete from where the name is equal to specific value
        # the "name" is unique to each row
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    # insert item or update existing item
    def put(self, name):
        data = Item.parser.parse_args()

        # find out if the item already exists
        item = self.find_by_name(name)

        # dictionary
        updated_item = {
            'name': name,
            'price': data['price']
        }

        # if there is no item, create a new item
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        # else if item already exists, update the item
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred inserting the item"}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # update items table and set the price where the name is equal to something
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

# return list of all our items
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # select everything from items table
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return{'items': items}
