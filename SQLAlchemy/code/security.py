# safe string compare instead of using '=='
from werkzeug.security import safe_str_cmp

from models.user import UserModel

# authenticate the user
def authenticate(username, password):
    # find username by mapping
    # if no user with that username in mapping, return 'None'
    user = UserModel.find_by_username(username)
    # if user and user's password equals the password, return the user
    if user and safe_str_cmp(user.password, password):
        return user

# payload is contents of JWT token
def identity(payload):
    # extract user ID from the payload
    user_id = payload['identity']
    # retrieve specific user
    return UserModel.find_by_id(user_id)
