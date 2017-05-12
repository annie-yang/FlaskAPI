# CRUD
# Create -- post
# Read -- get
# Update -- put
# Delete -- delete

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
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # internal server error

        # return the item to DB
        # HTTP status code '201' means object has been created
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        # if item exists, delete from DB
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    # insert item or update existing item
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        # if there is no item, create a new item
        if item is None:
            item = ItemModel(name, data['price'])
        # else if item already exists, update the item
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

# return list of all our items
class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
        # another option: list(map(lambda x: x.json(), ItemModel.query.all()))}
