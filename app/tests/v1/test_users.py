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

    def test_user_registration(self, path="api/v1/auth/signup", data={}):
        pass