from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.storemodel import StoreModel


class StoreList(Resource):
    def get(self):
        result = StoreModel.query.order_by(StoreModel.id).all()
        stores = []
        for row in result:
            stores.append({'id': row.id, 'name': row.name})
        return {'stores': stores}


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help="Name is required"
    )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message': "The store '{}' is already exist".format(name)}, 400
        data = Store.parser.parse_args()
        new_store = StoreModel(None, data['name'])
        try:
            new_store.save_to_db()
            new_store = StoreModel.find_by_name(name)
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # Internal Server Error
        return new_store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {'Message': "The store '{}' is not exist".format(name)}, 404
        try:
            store.delete_from_db()
        except:
            return {'message': 'An error occurred deleting the store'}, 500  # Internal Server Error
        return {'message': "The store '{}' has been deleted".format(name)}

    def put(self, name):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(name)

        if store is None:
            new_item = StoreModel(None, name, data['price'], data['store_id'])
            try:
                new_item.save_to_db()
                new_item = StoreModel.find_by_name(name)
            except:
                return {'message': 'An error occurred inserting the store'}, 500  # Internal Server Error
            return new_item.json(), 201

        else:
            store.price = data['price']
            store.store_id = data['store_id']
            try:
                store.save_to_db()
                store = StoreModel.find_by_name(name)
            except:
                return {'message': 'An error occurred updating the store'}, 500  # Internal Server Error
        return {'message': "Updated successfully", 'store': store.json()}
