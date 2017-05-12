from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'fjewiojfeiowj'
api = Api(app)

# JWT creates a new endpoint (/auth)
# when '/auth' is called, we send username and password
# JWT then sends the username and password to authentication
# finds correct user and password and compares from the one we received through auth
# if matches, return the user
jwt = JWT(app, authenticate, identity)

# contains each dictionary for each item
# temporary DB
items = []

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
    # look into the array and retrieve the item that matches the requested name
    def get(self, name):
        # filter the list of items in the 'DB' --> one parameter ('items')
        # 'items' is the list of items we are filtering
        # go through each item, execute each item, and see if the items name matches the parameter name (in this case, 'items')
        # 'next' gives us the first item found by the filter function
        # if can't find an item, it will return 'None'
        item = next(filter(lambda x: x['name'] == name, items), None)

        # if no item is found, send "None"
        # if item exists, return HTTP error status code 200, else return 404
        return {'item': item}, 200 if item else 404

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

# access Student API
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# run on port and show error message
app.run(port=5000, debug=True)
