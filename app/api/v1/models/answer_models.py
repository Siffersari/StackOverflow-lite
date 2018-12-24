from flask import jsonify
from .question_models import questions


class AnswerModels(object):
    """
    This class AnswerModels contains methods that allow 
    posting, getting and updating of answers.
    """
    def __init__(self):
        self.db = questions

    
    def get_answers(self, username, questionId):
        userFound, imHere, answerFound = False, False, False
        position = 0        
        for user in range(len(self.db)):
            for key, value in self.db[user].items():
                if key == username:
                    userFound = True
                    position = user
                    for question, content in value.items():
                        if question == int(questionId):
                            imHere = True
                            for name, body in content.items():
                                if name == "answers":
                                    if body:
                                        answerFound = True

        if not userFound:
            return jsonify({"Err": "This user is not found. Please check your username."}), 404

        elif userFound:
            if not imHere:
                return jsonify({"Err": "This question is not found."}), 404
            elif imHere:
                if not answerFound:
                    return jsonify({"Err": "No answer has been found"}), 404

        return jsonify({"Answers": self.db[position][username][int(questionId)]["answers"]})



    def post_answer(self, username, answer, questionId, answerId):
        userFound, imHere, answerFound, answerPosted = False, False, False, False
        position = 0
        for user in range(len(self.db)):
            for key, value in self.db[user].items():
                if key == username:
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
                    self.db[position][username][int(questionId)]["answers"] = {
                        int(answerId): {answer: False}
                    }
                    return jsonify({"Success": "Your answer has been received"}), 201
                elif answerFound and answerPosted:
                    return jsonify({"Err": "This answer exists already"}), 400

        self.db[position][username][int(questionId)]["answers"][int(answerId)] = {
            answer: False}
        return jsonify({"Success": "You answer has been posted."}), 201




    def select_answer(self, username, answer, questionId, answerId):
        userFound, imHere, answerFound, answerPosted, answerMatches = False, False, False, False, False
        position = 0
        for user in range(len(self.db)):
            for key, value in self.db[user].items():
                if key == username:
                    userFound = True
                    position = user
                    for question, content in value.items():
                        if question == int(questionId):
                            imHere = True
                            for name, content in content.items():
                                if name == "answers":
                                    answerFound = True
                                    for item, data in content.items():
                                        if item == int(answerId):
                                            answerPosted = True
                                            for answerHere in data.keys():
                                                if answerHere == answer:
                                                    answerMatches = True
                                                    break

        if not userFound:
            return jsonify({"Err": "This user is not found. Please check your username."}), 404

        elif userFound:
            if not imHere:
                return jsonify({"Err": "This question is not found."}), 404
            elif imHere:
                if not answerFound:
                    self.db[position][username][int(questionId)]["answers"] = {
                        int(answerId): {answer: False}
                    }
                    return jsonify({"Success": "Your answer has been received"}), 201
                elif answerFound and answerPosted:
                    if not answerMatches:
                        self.db[position][username][int(questionId)]["answers"][int(answerId)] = {
                            answer: False}
                        return jsonify({"Success": "Answer updated!"})

        self.db[position][username][int(
            questionId)]["answers"][int(answerId)][answer] = True
        return jsonify({"Success": " '{}' has been accepted!".format(answer)})
