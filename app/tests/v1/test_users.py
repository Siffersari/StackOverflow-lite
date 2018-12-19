import unittest
import json
from ... import create_app


class TestUsers(unittest.TestCase):
    """ 
    Tests for user data validation, registration and login funtionality 
    authored by Leewel Karani
    """

    def setUp(self):
        """ 
        Setup what the test will need to run efficiently
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.data = {
            "fName": "Daisy",
            "lName": "Flower",
            "uname": "Daisy",
            "email": "Daisy@gmail.com",
            "password": "D@1sies"
        }
        self.wrongEmail = {
            "fName": "Daisy",
            "lName": "Flower",
            "uname": "Daisy",
            "email": "Daisygmail.com",
            "password": "D@1sies"
        }
        self.wrongPass = {
            "fName": "Daisy",
            "lName": "Flower",
            "uname": "Daisy",
            "email": "Daisy@gmail.com",
            "password": "D@sies"
        }
        self.wrongName = {
            "fName": "Dai",
            "lName": "Flower",
            "uname": "Daisy",
            "email": "Daisy@gmail.com",
            "password": "D@1sies"
        }
        self.wrongUname = {
            "fName": "Dai",
            "lName": "Flower",
            "uname": "Dasy",
            "email": "Daisy@gmail.com",
            "password": "D@1sies"
        }

    def register_user(self, path="api/v1/auth/signup", data={}):
        """ Registers a new user with given data or default if not provided """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def login_user(self, path="api/v1/auth/login", data={}):
        """ Logs in a user """
        if not data:
            data = self.data

        self.register_user()

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def test_register_users(self):
        """ Tests for user registration cases and validation of user data """
        new_user = self.register_user()
        userEmail = self.register_user(data=self.wrongEmail)
        userPass = self.register_user(data=self.wrongPass)
        userBadName = self.register_user(data=self.wrongName)
        userUname = self.register_user(data=self.wrongUname)
        self.assertEqual(new_user.status_code, 201)
        self.assertEqual(userEmail.status_code, 400)
        self.assertEqual(userBadName.status_code, 400)
        self.assertEqual(userPass.status_code, 400)
        self.assertEqual(userUname.status_code, 400)
        self.assertTrue(userEmail.json["Err"])
        self.assertTrue(userPass.json["Err"])
        self.assertTrue(userBadName.json["Err"])
        self.assertTrue(userUname.json["Err"])

    def test_login_users(self):
        """ Tests for user login cases and validation of data """
        self.assertEqual(self.login_user().status_code, 200)
        self.assertEqual(self.login_user(
            data=self.wrongUname).status_code, 400)
        self.assertEqual(self.login_user(data=self.wrongPass).status_code, 400)
        self.assertTrue(self.login_user(data=self.wrongPass).json["Err"])
        self.assertTrue(self.login_user(data=self.wrongUname).json["Err"])
        self.assertTrue(self.login_user().json["Success"])
