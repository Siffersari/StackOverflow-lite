from flask import Flask, request, jsonify

from .. import version1

from .question_views import questions


@version1.route("/questions/<questionId>/answers", methods=['POST'])
def postAnswer(questionId):
    userFound, imHere, answerFound, answerPosted = False, False, False, False
    position = 0
    userName = request.get_json()["uname"]
    answer = request.get_json()["answer"]
    answerId = request.get_json()["answerId"]

    for user in range(len(questions)):
        for key, value in questions[user].items():
            if key == userName:
                userFound = True
                position = user
                for question, content in value.items():
                    if question == int(questionId):
                        imHere = True
                        for name, content in content.items():
                            if name == "answers":
                                answerFound = True
                                for item in content.keys():
                                    if item == int(answerId):
                                        answerPosted = True
                                        break

    if not userFound:
        return jsonify({"Err": "This user is not found. Please check your username."}), 404

    elif userFound:
        if not imHere:
            return jsonify({"Err": "This question is not found."}), 404
        elif imHere:
            if not answerFound:
                questions[position][userName][int(questionId)]["answers"] = {
                    int(answerId): {answer: False}
                }
                return jsonify({"Success": "Your answer has been received"})
            elif answerFound and answerPosted:
                return jsonify({"Err": "This answer exists already"}), 400

    questions[position][userName][int(questionId)]["answers"][int(answerId)] = {
        answer: False}
    return jsonify({"Success": "You answer has been posted."})


@version1.route("/questions/<questionId>/answers", methods=['GET'])
def getAnswers(questionId):
    """ Gets all answers to a question """
    userFound, imHere, answerFound = False, False, False
    position = 0
    userName = request.get_json()["uname"]
   
    for user in range(len(questions)):
        for key, value in questions[user].items():
            if key == userName:
                userFound = True
                position = user
                for question, content in value.items():
                    if question == int(questionId):
                        imHere = True
                        for name, content in content.items():
                            if name == "answers":
                                answerFound = True
                                

    if not userFound:
        return jsonify({"Err": "This user is not found. Please check your username."}), 404

    elif userFound:
        if not imHere:
            return jsonify({"Err": "This question is not found."}), 404
        elif imHere:
            if not answerFound:
                return jsonify({"Err": "No answer has been found"}), 404

        
        
    return jsonify(questions[position][userName][int(questionId)]["answers"])
    
