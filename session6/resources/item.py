import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.itemmodal import ItemModal


class ItemList(Resource):
    table_name = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} ".format(table=self.table_name)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}


class Item(Resource):
    table_name = 'items'
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModal.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModal.find_by_name(name):
            return {'Message': "The item '{}' is already exist".format(name)}, 400
        data = Item.parser.parse_args()
        new_item = ItemModal(None, name, data['price'])
        try:
            new_item.create()
            new_item = ItemModal.find_by_name(name)
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # Internal Server Error
        return new_item.json(), 201

    def delete(self, name):
        if ItemModal.find_by_name(name) is None:
            return {'Message': "The item '{}' is not exist".format(name)}, 404
        try:
            ItemModal.delete(name)
        except:
            return {'message': 'An error occurred deleting the item'}, 500  # Internal Server Error
        return {'message': "The item '{}' has been deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()
        updated_item = ItemModal(None, name, data['price'])

        if ItemModal.find_by_name(name) is None:
            new_item = ItemModal(None, name, data['price'])
            try:
                new_item.create()
                new_item = ItemModal.find_by_name(name)
            except:
                return {'message': 'An error occurred inserting the item'}, 500  # Internal Server Error
            return new_item.json(), 201

        else:
            try:
                updated_item.update()
                updated_item = ItemModal.find_by_name(name)
            except:
                return {'message': 'An error occurred updating the item'}, 500  # Internal Server Error
        return {'message': "Updated successfully", 'item': updated_item.json()}
