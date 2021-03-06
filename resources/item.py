from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.itemmodel import ItemModel


class ItemList(Resource):
    def get(self):
        result = ItemModel.query.order_by(ItemModel.id).all()
        items = []
        for row in result:
            items.append(row.json())
        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Price is required"
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Store ID is required"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'Message': "The item '{}' is already exist".format(name)}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(None, name, data['price'], data['store_id'])
        try:
            new_item.save_to_db()
            new_item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # Internal Server Error
        return new_item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'Message': "The item '{}' is not exist".format(name)}, 404
        try:
            item.delete_from_db()
        except:
            return {'message': 'An error occurred deleting the item'}, 500  # Internal Server Error
        return {'message': "The item '{}' has been deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            new_item = ItemModel(None, name, data['price'], data['store_id'])
            try:
                new_item.save_to_db()
                new_item = ItemModel.find_by_name(name)
            except:
                return {'message': 'An error occurred inserting the item'}, 500  # Internal Server Error
            return new_item.json(), 201

        else:
            item.price = data['price']
            item.store_id = data['store_id']
            try:
                item.save_to_db()
                item = ItemModel.find_by_name(name)
            except:
                return {'message': 'An error occurred updating the item'}, 500  # Internal Server Error
        return {'message': "Updated successfully", 'item': item.json()}
