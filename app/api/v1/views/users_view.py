from flask import Flask, request
from .. models.user_model import UserModels
from .. import version1

db = UserModels()


@version1.route("/")
def hello_world():
    """ Returns 'hello world' """
    return "hello World"


@version1.route("/users", methods=["GET"])
def get_users():
    """ Gets all registered users """
    return db.fetch_users()


@version1.route("/auth/signup", methods=["POST"])
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
    return db._validator(user)


@version1.route("/auth/login", methods=['POST'])
def loginUser():
    """ logs in a registered user """
    password = request.get_json()["password"]
    userName = request.get_json()["uname"]

    return db.login_user(userName, password)
