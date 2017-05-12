from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# inheritance
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'fjewiojfeiowj'
api = Api(app)

# JWT creates a new endpoint (/auth)
# when '/auth' is called, we send username and password
# JWT then sends the username and password to authentication
# finds correct user and password and compares from the one we received through auth
# if matches, return the user
jwt = JWT(app, authenticate, identity)

# access Student API
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# run on port and show error message
# run flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
