from flask_restful import Resource, reqparse

from models.usermodel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "User is already exists"}, 400
        try:
            new_user = UserModel(None, data['username'], data['password'])
            new_user.insert_to_db()
            new_user = UserModel.find_by_username(data['username'])
        except:
            return {'message': 'An error occurred register user '}, 500  # Internal Server Error
        return {
                "message": "User created successfully",
                "user": {
                    "user_id": new_user.id,
                    "user_name": new_user.username,
                    }
                }, 201
