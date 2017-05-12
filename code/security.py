# safe string compare instead of using '=='
from werkzeug.security import safe_str_cmp

from user import User

# memory table of all our users
users = [
    User(1, 'bob', 'asdf')
]

# assigning key value pair
# retrieve user by username and id
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

# authenticate the user
# compare user's password/username with mapping password/username
def authenticate(username, password):
    # find username by mapping
    # if no user with that username in mapping, return 'None'
    user = username_table.get(username, None)
    # if user and user's password equals the password, return the user
    if user and safe_str_cmp(user.password, password):
        return user

# payload is contents of JWT token
def identity(payload):
    # extract user ID from the payload
    user_id = payload['identity']
    # retrieve specific user
    return userid_mapping.get(user_id, None)
