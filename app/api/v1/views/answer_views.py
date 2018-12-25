from flask import Flask, request
from .. models.answer_models import AnswerModels
from .. import version1


db = AnswerModels()


@version1.route("/questions/<questionId>/answers", methods=['POST'])
def postAnswer(questionId):
    
    userName = request.get_json()["uname"]
    answer = request.get_json()["answer"]
    answerId = request.get_json()["answerId"]

    return db.post_answer(userName, answer, questionId, answerId)


@version1.route("/questions/<questionId>/answers", methods=['GET'])
def getAnswers(questionId):
    """ Gets all answers to a question """
    userName = request.get_json()["uname"]

    return db.get_answers(userName, questionId)

@version1.route("/questions/<questionId>/answers/<answerId>", methods=['PUT'])
def acceptAnswer(questionId, answerId):
    """ Marks an answer as accepted or updates an answer """
    
    answer = request.get_json()["answer"]
    userName = request.get_json()["uname"]

    return db.select_answer(userName, answer, questionId, answerId)