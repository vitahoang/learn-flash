from flask import Flask
from flask_jwt import JWT
from flask_restful import Api, Resource
from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}


api.add_resource(HelloWorld, '/')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000)
