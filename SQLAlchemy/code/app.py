from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

# inheritance
from security import authenticate, identity
# looks in resources package (folder) and finds the file
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# don't track every changes made by Flask SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
