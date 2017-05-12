# CRUD
# Create -- post
# Read -- get
# Update -- put
# Delete -- delete

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    # creating items
    def post(self,name):
        # return item if it already exists (from function "find_by_name")
        # make sure item is not already in the DB
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)},400 # something went wrong with request

        # parses data
        data = Item.parser.parse_args()

        # JSON data
        item = ItemModel(
            name,
            data['price']
        )

        # exception block
        try:
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error

        # return the item to DB
        # HTTP status code '201' means object has been created
        return item.json(), 201

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

        item = ItemModel.find_by_name(name)

        # dictionary
        updated_item = ItemModel(
            name,
            data['price']
        )

        # if there is no item, create a new item
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item"}, 500
        # else if item already exists, update the item
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred inserting the item"}, 500
        return updated_item.json()

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
