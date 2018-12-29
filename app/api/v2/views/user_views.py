from flask import Flask, request, jsonify
from .. models.user_models import UserModel
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from werkzeug.security import check_password_hash
from ...v2 import version2


def _validator(user):
    """ Validates user details before adding them """
    import re
    for key, value in user.items():
        if not value:
            return jsonify({"Err": "{} is a required field.".format(key)}), 400

        if (key == 'email' and not re.search(r'\w+[.|\w]\w+@\w+[.]\w+[.|\w+]\w+', value)):
            return jsonify({"Err": "Please enter a valid {}.".format(key)}), 400

        if (key == 'first_name' or key == 'last_name' or key == 'username') and (len(value) < 4 or len(value) > 15):
            return jsonify({"Err": "{} should be 4-15 characters long".format(key)}), 400

        if key == 'password':

            if not (len(re.findall(r'[A-Z]', value)) > 0 and len(re.findall(
                    r'[a-z]', value)) > 0 and len(re.findall(r'[0-9]', value)) > 0 and len(re.findall(r'[@#$]', value)) > 0):

                return jsonify({"Err": "{} should contain atleast one number, uppercase, lowercase and special character".format(key)}), 400


@version2.route("/")
def hello_world():
    """ Returns 'hello world' """
    return "hello World"


@version2.route("/users", methods=["GET"])
def get_users():
    """ Gets all registered users """
    resp = UserModel().get_all_users()

    return resp


@version2.route("/auth/signup", methods=["POST"])
def registerUser():
    """ Registers a user """
    firstName = request.get_json()["first_name"]
    lastName = request.get_json()["last_name"]
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    user = {
        "first_name": firstName,
        "last_name": lastName,
        "username": username,
        "email": email,
        "password": password
    }
# Then we validate user here.
    _validator(user)
    user_model = UserModel(**user)

    try:
        saved = user_model.save_user()
        if not saved:
            raise ValueError
    except ValueError:
        raise Forbidden("The username already exists")

    user_id = saved

    resp = {
        "message": "User signed up successfully",
        "username": username,
        "user_id": "{}".format(user_id)
    }

    user_model.close_db()

    return resp, 201


@version2.route("/auth/login", methods=['POST'])
def loginUser():
    """ logs in a registered user """
    password = request.get_json()["password"]
    username = request.get_json()["username"]

    user_details = {
        "username": username,
        "password": password
    }

    user = UserModel(**user_details)

    record = user.get_user_by_username(user_details["username"])

    if not record:
        raise Unauthorized('Your details were not found, please sign up')

    fname, lname, pwordhash = record

    if not check_password_hash(pwordhash, user_details["password"]):
        raise Unauthorized("The username or password is incorrect")

    name = "{}, {}".format(lname, fname)

    resp = {
        "message": "success",
        "name": name
    }

    return resp
