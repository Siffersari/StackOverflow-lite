from flask import Flask, request
from .. models.question_models import QuestionModels
from .. import version1

db = QuestionModels()


@version1.route("/questions", methods=["GET"])
def fetchQuestions():
    """ Fetches all questions """
    return db.get_all_questions()


@version1.route("/questions", methods=["POST"])
def postQuestion():
    """ Posts a question """
    title = request.get_json()["title"]
    body = request.get_json()["body"]
    questionId = request.get_json()["questionId"]
    userName = request.get_json()["uname"]

    return db.post_question(title, body, userName, questionId)


@version1.route("/questions/<questionId>", methods=["GET"])
def getQuestion(questionId):
    """ Gets a specific question """
    userName = request.get_json()["uname"]

    return db.get_specific_question(userName, questionId)


@version1.route("/questions/<questionId>", methods=["DELETE"])
def deleteQuestion(questionId):
    """ Deletes a specific question """
    userName = request.get_json()["uname"]

    return db.deleteQuestion(userName, questionId)
