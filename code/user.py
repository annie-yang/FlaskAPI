# user objects
class User(object):
    # store of data
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
