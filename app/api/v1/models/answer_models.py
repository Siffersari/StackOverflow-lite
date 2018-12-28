from flask import jsonify
from .question_models import questions


class AnswerModels(object):
    """
    This class AnswerModels contains methods that allow 
    posting, getting and updating of Answers.
    """

    def __init__(self):
        self.db = questions

    def check_database(self, username, answer, questionId, answerId):
        userFound, position, imHere, answerFound, answerPosted, answerMatches = False, 0, False, False, False, False
        result = []
        try:
            data = [[ind, question[username][int(questionId)]] for [ind,question] in enumerate(questions) if username in question.keys()]

        except:
            return True, position, imHere, answerFound, answerPosted, answerMatches

        if len(data) < 1:
            return userFound, position, imHere, answerFound, answerPosted, answerMatches
        else:
            userFound, imHere, position = True, True, data[0][0]
            
            

        if "Answers" in data[0][1].keys():
            answerFound = True
            if int(answerId) in data[0][1]["Answers"].keys():
                answerPosted = True
                if answer in data[0][1]["Answers"][int(answerId)].keys():
                    answerMatches = True
            
        else:
            return userFound, position, imHere, answerFound, answerPosted, answerMatches

        result = [userFound, position, imHere, answerFound, answerPosted, answerMatches]
        return result


    def get_answers(self, username, questionId):
        answer, answerId = "", 0

        results = self.check_database(username, answer, questionId, answerId)

        userFound, position, imHere, answerFound, answerPosted, answerMatches = results

        if not userFound:
            return jsonify({"Err": "This user is not found. Please check your username."}), 404

        elif userFound:
            if not imHere:
                return jsonify({"Err": "This question is not found."}), 404

            elif imHere:
                if not answerFound:
                    return jsonify({"Err": "No answer has been found"}), 404

        return jsonify({"Answers": self.db[position][username][int(questionId)]["Answers"]})

    def post_answer(self, username, answer, questionId, answerId):

        results = self.check_database(username, answer, questionId, answerId)

        userFound, position, imHere, answerFound, answerPosted, answerMatches = results

        if not userFound:
            return jsonify({"Err": "This user is not found. Please check your username."}), 404

        elif userFound:
            if not imHere:
                return jsonify({"Err": "This question is not found."}), 404

            elif imHere:
                if not answerFound:
                    self.db[position][username][int(questionId)]["Answers"] = {
                        int(answerId): {answer: False}
                    }
                    return jsonify({"Success": "Your answer has been received"}), 201

                elif answerFound and answerPosted:
                    return jsonify({"Err": "This answer exists already"}), 400

        self.db[position][username][int(questionId)]["Answers"][int(answerId)] = {
            answer: False}
        return jsonify({"Success": "You answer has been posted."}), 201

    def select_answer(self, username, answer, questionId, answerId):

        results = self.check_database(username, answer, questionId, answerId)

        userFound, position, imHere, answerFound, answerPosted, answerMatches = results

        if not userFound:
            return jsonify({"Err": "This user is not found. Please check your username."}), 404

        if not imHere:
            return jsonify({"Err": "This question is not found."}), 404

        elif imHere:
            if not answerFound:
                self.db[position][username][int(questionId)]["Answers"] = {
                    int(answerId): {answer: False}
                }
                return jsonify({"Success": "Your answer has been received and posted"}), 201

            elif (answerFound):
                if not answerPosted:
                    self.db[position][username][int(questionId)]["Answers"][int(answerId)] = {
                        answer: False}
                    return jsonify({"Success": "Your answer has been posted"}), 201

                elif answerPosted:
                    if not answerMatches:
                        self.db[position][username][int(questionId)]["Answers"][int(answerId)] = {
                            answer: False}
                        return jsonify({"Success": "Answer updated!"})

        self.db[position][username][int(
            questionId)]["Answers"][int(answerId)][answer] = True
        return jsonify({"Success": " '{}' has been accepted!".format(answer)})
