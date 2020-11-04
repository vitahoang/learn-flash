from flask import Flask
from flask_jwt import JWT
from flask_restful import Api, Resource

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth


@app.before_first_request
def create_db():
    db.create_all()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}


api.add_resource(HelloWorld, '/')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)
