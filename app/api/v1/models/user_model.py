# We store all our users here in an array.

users = [{
    "email": "Leewelkarani@gmail.com",
    "fName": "Leewel",
    "lName": "Karani",
    "password": "Pa$5word",
    "uname": "Leewel"
},
    {
    "email": "Johnjohn@gmail.com",
    "fName": "John",
    "lName": "john",
    "password": "J0#ndoe",
    "uname": "John"
}
]


class UserModels(object):
    """ This class Users contains the methods used while
    interacting with users and manipulating user details.
    """
    def __init__(self):
        self.db = users
