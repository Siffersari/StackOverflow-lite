import unittest
import json
from ... import create_app


class TestAnswers(unittest.TestCase):
    """
    Contains test cases for the questions
    """

    def setUp(self):
        """
        Initiates the app and varibles to be used when the tests run 
        """
        self.app = create_app()
        self.client = self.app.test_client()

        # Dummy data
        self.data = {
            "uname": "Leewel",
            "answer": "This is the 1st answer",
            "questionId": 3,
            "answerId": 1
        }
        

    def post_answer(self, path="/api/v1/questions/<questionId>/answers", data={}):
        """ Posts a question """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def fetch_answer(self, path="/api/v1/questions/<questionId>/answers"):
        """ Retreives all questions """
        response = self.client.get(path)
        return response

    def accept_answer(self, path="/api/v1/questions/<questionId>/answers", data={}):
        """ Retreives a specific quesiton given an Id """
        if not data:
            data = self.data
        response = self.client.put(path, data=json.dumps(
            data), content_type="application/json")
        return response