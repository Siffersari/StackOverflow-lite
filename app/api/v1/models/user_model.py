from flask import jsonify

# We store all our users here in an array, users.

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

    def fetch_users(self):
        return self.db

    def login_user(self, username, password):
        passMatch, unameMatch = False, False
        for user in range(len(self.db)):
            for key, value in self.db[user].items():
                if key == "uname":
                    if value == username:
                        unameMatch = True
                        if self.db[user]["password"] == password:
                            passMatch = True
                            break
    
        if not unameMatch:
            return jsonify({"Err": "Please check your username"}), 400
        if not passMatch:
            return jsonify({"Err": "Please check your password"}), 400

        return jsonify({"Success": "Welcome {}, You have been successfully logged in.".format(username)})


    def _validator(self, user):
        """ Validates user details before adding them """
        import re
        for key, value in user.items():
            if not value:
                return jsonify({"Err": "{} is a required field.".format(key)}), 400

            elif key == 'email':
                if not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', value):
                    return jsonify({"Err": "Please enter a valid {}.".format(key)}), 400

            elif key == 'fName' or key == 'lName' or key == 'uname':
                if (len(value) < 4 or len(value) > 15):
                    return jsonify({"Err": "{} should be 4-15 characters long".format(key)}), 400

            elif key == 'password':
                upper, lower = len(re.findall(
                    r'[A-Z]', value)), len(re.findall(r'[a-z]', value))
                digit, special = len(re.findall(
                    r'[0-9]', value)), len(re.findall(r'[@#$]', value))
                if not (upper and lower and digit and special):
                    return jsonify({"Err": "{} should contain atleast one number, uppercase, lowercase and special character".format(key)}), 400

        self.db.append(user)

        return jsonify(user), 201

