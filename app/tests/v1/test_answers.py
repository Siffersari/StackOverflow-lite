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
            "questionId": 1,
            "answerId": 1
        }
        self.data1 = {
            "uname": "Leewel",
            "answer": "This is the 1st answer",
            "questionId": 1,
            "answerId": 2
        }
        self.data2 = {
            "uname": "Leewel",
            "answer": "This is the 1st answer",
            "questionId": 2,
            "answerId": 1
        }
        self.data3 = {
            "uname": "Nani",
            "answer": "This is the 1st answer",
            "questionId": 1,
            "answerId": 1
        }
        self.data4 = {
            "uname": "Leewel",
            "answer": "This is the 1st answer",
            "questionId": 3,
            "answerId": 1
        }
        self.data5 = {
            "uname": "Leewel",
            "answer": "This is the 1st answer",
            "questionId": 2,
            "answerId": 2
        }
        self.data6 = {
            "uname": "Janet",
            "answer": "This is the 1st answer",
            "questionId": 2,
            "answerId": 1
        }
        self.data7 = {
            "uname": "Janet",
            "answer": "This is the 1st answer",
            "questionId": 3,
            "answerId": 3
        }
        self.data8 = {
            "uname": "Leewel",
            "answer": "This is the 1st answer",
            "questionId": 1,
            "answerId": 3
        }
        self.data9 = {
            "uname": "Leewel",
            "answer": "This is the an updated answer",
            "questionId": 1,
            "answerId": 1
        }

    def post_answer(self, path="/api/v1/questions/<questionId>/answers", data={}):
        """ Posts a question """
        if not data:
            data = self.data

        response = self.client.post(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def fetch_answers(self, path="/api/v1/questions/<questionId>/answers", data={}):
        """ Retreives all questions """
        if not data:
            data = self.data
        response = self.client.get(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def accept_answer(self, path="/api/v1/questions/<questionId>/answers", data={}):
        """ Retreives a specific quesiton given an Id """
        if not data:
            data = self.data
        response = self.client.put(path, data=json.dumps(
            data), content_type="application/json")
        return response

    def test_posts_new_answer_if_existing_user(self):
        self.assertEqual(self.post_answer(
            path="/api/v1/questions/{}/answers".format(self.data["questionId"])).status_code, 201)
        self.assertTrue(self.post_answer(path="/api/v1/questions/{}/answers".format(
            self.data2["questionId"]), data=self.data2).json["Success"])

    def test_posts_new_answer_if_user_question_answers_found(self):
        self.assertEqual(self.post_answer(path="/api/v1/questions/{}/answers".format(
            self.data1["questionId"]), data=self.data1).status_code, 201)
        self.assertTrue(self.post_answer(path="/api/v1/questions/{}/answers".format(
            self.data5["questionId"]), data=self.data5).json["Success"])

    def test_returns_error_if_missing_user(self):
        self.assertEqual(self.post_answer(
            path="/api/v1/questions/{}/answers".format(self.data3), data=self.data3).status_code, 404)
        self.assertTrue(self.post_answer(path="/api/v1/questions/{}/answers".format(
            self.data3["questionId"]), data=self.data3).json["Err"])

    def test_returns_error_if_missing_question(self):
        self.assertEqual(self.post_answer(path="/api/v1/questions/{}/answers".format(
            self.data4["questionId"]), data=self.data4).status_code, 404)
        self.assertTrue(self.post_answer(path="/api/v1/questions/{}/answers".format(
            self.data4["questionId"]), data=self.data4).json["Err"])

    def test_returns_error_if_existing_answer(self):
        self.assertEqual(self.post_answer(
            path="/api/v1/questions/{}/answers".format(self.data["questionId"])).status_code, 400)
        self.assertTrue(self.post_answer(
            path="/api/v1/questions/{}/answers".format(self.data["questionId"])).json["Err"])

    def test_fetches_existing_answers(self):
        answer = self.post_answer(
            path="api/v1/questions/{}/answers".format(self.data6["questionId"]), data=self.data6)
        self.assertEqual(answer.status_code, 201)
        self.assertEqual(self.fetch_answers(path="/api/v1/questions/{}/answers".format(
            self.data6["questionId"]), data=self.data6).status_code, 200)
        self.assertTrue(self.fetch_answers(path="/api/v1/questions/{}/answers".format(
            self.data6["questionId"]), data=self.data6).json["Answers"])
        self.assertNotEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data6["questionId"], self.data6["answerId"]), data=self.data6).status_code, 404)

    def test_returns_error_if_question_missing(self):
        self.assertEqual(self.fetch_answers(path="/api/v1/questions/{}/answers".format(
            self.data7["questionId"]), data=self.data7).status_code, 404)
        self.assertTrue(self.fetch_answers(path="/api/v1/questions/{}/answers".format(
            self.data7["questionId"]), data=self.data7).json["Err"])
        self.assertNotEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data7["questionId"], self.data7["answerId"]), data=self.data7).status_code, 200)

    def test_accept_answer(self):
        answer = self.post_answer(
            path="api/v1/questions/{}/answers".format(self.data8["questionId"]), data=self.data8)
        self.assertEqual(answer.status_code, 201)
        #self.assertEqual(answer.json, "201")
        #self.assertTrue(self.fetch_answers(path="/api/v1/questions/{}/answers".format(self.data["questionId"]), data=self.data).json["Answers"]["3"])
        self.assertEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data8["questionId"], self.data8["answerId"]), data=self.data8).status_code, 200)
        self.assertTrue(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data8["questionId"], self.data8["answerId"]), data=self.data8).json["Success"])
        self.assertNotEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data8["questionId"], self.data8["answerId"]), data=self.data8).status_code, 404)

    def test_returns_error_if_not_user_found(self):
        #self.assertTrue(self.fetch_answers(path="/api/v1/questions/{}/answers".format(self.data3["questionId"]), data=self.data3).json["Answers"])
        self.assertEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data3["questionId"], self.data3["answerId"]), data=self.data3).status_code, 404)
        self.assertTrue(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data3["questionId"], self.data3["answerId"]), data=self.data3).json["Err"])
        self.assertNotEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data3["questionId"], self.data3["answerId"]), data=self.data3).status_code, 200)

    def test_returns_error_if_not_question_found(self):
        self.assertEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data4["questionId"], self.data4["answerId"]), data=self.data4).status_code, 404)
        self.assertTrue(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data4["questionId"], self.data4["answerId"]), data=self.data4).json["Err"])
        self.assertNotEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data4["questionId"], self.data4["answerId"]), data=self.data4).status_code, 200)

    def test_updates_answer_if_answer_exists_but_diff_context(self):
        self.assertEqual(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data9["questionId"], self.data9["answerId"]), data=self.data9).status_code, 200)
        self.assertTrue(self.accept_answer(path="/api/v1/questions/{}/answers/{}".format(
            self.data9["questionId"], self.data9["answerId"]), data=self.data9).json["Success"])


    def tearDown(self):
        self.app = None

if __name__ == '__main__':
    unittest.main()