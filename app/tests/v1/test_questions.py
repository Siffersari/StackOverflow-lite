import unittest
import json
from ... import create_app


class TestQuestions(unittest.TestCase):
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
            "title": "Flask app blueprints",
            "body": "I registered my blueprints but when I run the app, I get a 404 status code respone.",
            "uname": "Jina",
            "questionId": 1
        }

        self.ExistUname = {
            "title": "Flask app blueprints",
            "body": "I registered my blueprints but when I run the app, I get a 404 status code respone.",
            "uname": "Leewel",
            "questionId": 1
        }

        self.nonExistId = {
            "title": "Flask app blueprints",
            "body": "I registered my blueprints but when I run the app, I get a 404 status code respone.",
            "uname": "Leewel",
            "questionId": 4
        }

        self.question1 = {
            "title": "Flask app blueprints",
            "body": "I registered my blueprints but when I run the app, I get a 404 status code respone.",
            "uname": "Nani",
            "questionId": 1
        }

        self.question2 = {
            "title": "Flask app blueprints",
            "body": "I registered my blueprints but when I run the app, I get a 404 status code respone.",
            "uname": "Alex",
            "questionId": 1
        }
        self.question3 = {
            "title": "Flask app blueprints",
            "body": "I registered my blueprints but when I run the app, I get a 404 status code respone.",
            "uname": "Dembele",
            "questionId": 1
        }

    def post_question(self, path="/api/v1/questions", data={}):
        """ Posts a question """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def fetch_questions(self, path="/api/v1/questions"):
        """ Retreives all questions """
        response = self.client.get(path)
        return response

    def delete_question(self, path="/api/v1/questions/<questionId>", data={}):
        """ Deletes a question """
        if not data:
            data = self.question1

        response = self.client.delete(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def test_post_question(self):
        """ Tests the post question endpoint posts a question """
        posted_question = self.post_question()
        post_existing = self.post_question(data=self.ExistUname)
        post_existing_newId = self.post_question(data=self.nonExistId)
        self.assertEqual(posted_question.status_code, 201)
        self.assertEqual(post_existing_newId.status_code, 201)
        self.assertEqual(post_existing.status_code, 400)
        self.assertTrue(posted_question.json["Success"])
        self.assertTrue(post_existing_newId.json["Success"])
        self.assertTrue(post_existing.json["Err"])

    def test_fetch_questions(self):
        """ Test get question endpoint gets all questions """
        self.assertEqual(self.fetch_questions().status_code, 200)
        self.assertNotEqual(self.fetch_questions().status_code, 404)
        self.assertTrue(self.fetch_questions().json["Questions"])

    def test_delete_question(self):
        """ Tests delete question endpoint deletes a question """
        post_question = self.post_question(data=self.question1)
        question3 = self.post_question(data=self.question3)
        self.assertEqual(post_question.status_code, 201)
        self.assertEqual(question3.status_code, 201)
        self.assertEqual(self.delete_question(
            path="/api/v1/questions/{}".format(self.question1["questionId"])).status_code, 200)
        self.assertTrue(self.delete_question(path="/api/v1/questions/{}".format(
            self.question3["questionId"]), data=self.question3).json["Success"])
        self.assertEqual(self.delete_question(
            path="/api/v1/questions/{}".format(self.question1["questionId"])).status_code, 404)
        self.assertEqual(self.delete_question(path="/api/v1/questions/{}".format(
            self.question2["questionId"]), data=self.question2).status_code, 404)
        self.assertTrue(self.delete_question(
            path="/api/v1/questions/{}".format(self.question1["questionId"])).json["Err"])
        self.assertTrue(self.delete_question(path="/api/v1/questions/{}".format(
            self.question2["questionId"]), data=self.question2).json["Err"])

    def tearDown(self):
        """ Destroys app and variable instances """
        self.app = None


if __name__ == '__main__':
    unittest.main()
