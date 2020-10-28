from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from session4.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'vita'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth

items = []


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'Message': "The item '{}' is already exist".format(name)}, 400
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "The item '{}' has been deleted".format(name)}

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'price',
            type=float,
            required=True,
            help="This field cannot be None"
        )
        data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item, 201
        if item:
            item['price'] = data['price']
            return item, 200


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(HelloWorld, '/')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
app.run(port=5000)
