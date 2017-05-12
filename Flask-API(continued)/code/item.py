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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        # if row exists, then return the name and price
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        # else return error message
        return {"message:" "Item not found"}, 404

    # creating items
    def post(self,name):
        # if next item is found
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            # return message
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # hard coded 'price'
        item = {
            'name': name,
            'price': data['price']
        }
        # add the item to the very end of 'items' list array
        items.append(item)

        # let the application know we created the item and added it to our 'DB'
        # HTTP status code '201' means object has been created
        return item, 201

    def delete(self, name):
        # items variable in this block is outer items variable
        global items
        # look for the elements in item, except one element, which that element would get deleted
        items = list(filter(lambda x: x['name'] != name, items))

        return {'message': 'Item deleted'}

    # create item or update existing item
    def put(self, name):
        data = Item.parser.parse_args()

        # find out if the item already exists
        item = next(filter(lambda x: x['name'] == name, items), None)

        # if there is no item, create a new item
        if item is None:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        # else if item already exists, update the item
        else:
            item.update(data)
        return item

# return list of all our items
class ItemList(Resource):
    def get(self):
        return {'items': items}
