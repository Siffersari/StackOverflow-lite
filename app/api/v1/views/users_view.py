from flask import Flask, request, jsonify

from .. import version1


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


def _validator(user):
    """ Validates user details before adding them """
    import re
    for key, value in user.items():
        if not value:
            return jsonify({"err": "{} is a required field.".format(key)}), 400

        elif key == 'email':
            if not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', value):
                return jsonify({"err": "Please enter a valid {}.".format(key)}), 400

        elif key == 'fName' or key == 'lName' or key == 'uname':
            if (len(value) < 4 or len(value) > 15):
                return jsonify({"err": "{} should be 4-15 characters long".format(key)}), 400

        elif key == 'password':
            upper, lower = len(re.findall(
                r'[A-Z]', value)), len(re.findall(r'[a-z]', value))
            digit, special = len(re.findall(
                r'[0-9]', value)), len(re.findall(r'[@#$]', value))
            if not (upper and lower and digit and special):
                return jsonify({"err": "{} should contain atleast one number, uppercase, lowercase and special character".format(key)}), 400

    users.append(user)

    return jsonify(user)


@version1.route("/")
def hello_world():
    """ Returns 'hello world' """
    return "hello World"


@version1.route("/users", methods=["GET"])
def get_users():
    """ Gets all registered users """
    return jsonify(users)


@version1.route("/signup", methods=["POST"])
def registerUser():
    """ Registers a user """
    firstName = request.get_json()["fName"]
    lastName = request.get_json()["lName"]
    userName = request.get_json()["uname"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    user = {
        "fName": firstName,
        "lName": lastName,
        "uname": userName,
        "email": email,
        "password": password
    }
# Then we return the '_validator' method here.
    return _validator(user)


@version1.route("/login", methods=['POST'])
def loginUser():
    """ logs in a registered user """
    passMatch, unameMatch = False, False
    password = request.get_json()["password"]
    userName = request.get_json()["uname"]
    for user in range(len(users)):
        for key, value in users[user].items():
            if key == "uname":
                if value == userName:
                    unameMatch = True
                    if users[user]["password"] == password:
                        passMatch = True
                        break
    
    if not unameMatch:
        return jsonify({"Err": "Please check your username"})
    if not passMatch:
        return jsonify({"Err": "Please check your password"})
    

    return jsonify({"Message": "Welcome {}, You have been successfully logged in.".format(userName)})
