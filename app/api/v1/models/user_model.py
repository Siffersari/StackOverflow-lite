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
        if not users:
            return jsonify({"Err": "There no registered users yet"}), 404

        return jsonify(self.db), 200

    def login_user(self, username, password):
        user = [user for user in users if user["uname"] == username]

        if len(user) < 1:
            return jsonify({"Err": "Please check your username"}), 400

        elif user[0]["password"] != password:
            return jsonify({"Err": "Please check your password"}), 400

        return jsonify({"Success": "Welcome {}, You have been successfully logged in.".format(username)})

    def _validator(self, user):
        """ Validates user details before adding them """
        import re
        for key, value in user.items():
            if not value:
                return jsonify({"Err": "{} is a required field.".format(key)}), 400

            if (key == 'email' and not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', value)):
                return jsonify({"Err": "Please enter a valid {}.".format(key)}), 400

            if (key == 'fName' or key == 'lName' or key == 'uname') and (len(value) < 4 or len(value) > 15):
                return jsonify({"Err": "{} should be 4-15 characters long".format(key)}), 400

            if key == 'password':

                if not (len(re.findall(r'[A-Z]', value)) > 0 and len(re.findall(
                        r'[a-z]', value)) > 0 and len(re.findall(r'[0-9]', value)) > 0 and len(re.findall(r'[@#$]', value)) > 0):

                    return jsonify({"Err": "{} should contain atleast one number, uppercase, lowercase and special character".format(key)}), 400

        self.db.append(user)

        return jsonify(user), 201
