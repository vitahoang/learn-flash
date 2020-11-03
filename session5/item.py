import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class ItemList(Resource):
    def get(self):
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

    @staticmethod
    def find_by_name(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE name=?".format(table=Item.table_name)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'id': row[0], 'name': row[1], 'price': row[2]}}

    @staticmethod
    def create_new_item(name):
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=Item.table_name)
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return item, 201

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {'Message': "The item '{}' is already exist".format(name)}, 400
        return self.create_new_item(name)

    def delete(self, name):
        if self.find_by_name(name) is None:
            return {'Message': "The item '{}' is not exist".format(name)}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM {table} WHERE name=?".format(table=Item.table_name)
        cursor.execute(query, name)
        connection.commit()
        connection.close()
        return {'message': "The item '{}' has been deleted".format(name)}

    def put(self, name):
        if self.find_by_name(name) is None:
            return self.create_new_item(name)
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE {table} SET price=? WHERE name=?".format(table=Item.table_name)
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()
        return {'message': "Updated successfully", 'item': item}

