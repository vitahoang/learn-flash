from models.usermodal import UserModal


def authenticate(username, password):
    user = UserModal.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModal.find_by_id(user_id)
