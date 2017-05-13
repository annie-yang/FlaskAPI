from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    # checks DB to see if store exists
    def get(self, name):
        store = StoreModel.find_by_name(name)

        # check if store exists
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    # checks to see if store name exists
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        # create a store if store name doesn't exist
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message':'An error occurred while creating the store'}, 500

        return store.json(), 201

    # look to see if store exists, if it does, delete store
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
