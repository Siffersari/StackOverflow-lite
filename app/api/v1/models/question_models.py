from flask import jsonify

# All questions stored here in an array, questions

questions = [
    {
        "Leewel":
        {
            1:
                {
                    "title": "Git won't upload my directory",
                    "body": "I have been trying to upload but I get a not authorized error."
                },
            2:
                {
                    "title": "Windows won't start after dualbooting Linux",
                    "body": "Hello guys, I installed Linux on my windows device, now it won't boot up"
                }

        }
    },

    {
        "Janet":
        {
            1:
                {
                    "title": "Git won't upload my directory",
                    "body": "I have been trying to upload but I get a not authorized error."
                },
            2:
                {
                    "title": "Windows won't start after dualbooting Linux",
                    "body": "Hello guys, I installed Linux on my windows device, now it won't boot up"
                }

        }
    }

]


class QuestionModels(object):
    """ This class, QuestionModels contains all the methods to
    post, get and update question(s).
    """

    def __init__(self):
        self.db = questions

    def check_database(self, username, questionId):
        userFound, imHere = False, False
        position = 0
        try:
            data = [[ind, question[username][int(questionId)]] for [ind,question] in enumerate(questions) if username in question.keys()]

        except:
            return True, position, imHere

        if len(data) < 1:
            return userFound, position, imHere
        else:
            userFound, imHere, position = True, True, data[0][0]

        return userFound, position, imHere

    def get_all_questions(self):
        if not self.db:
            return jsonify({"Err": "There are no existing questions"}), 404

        return jsonify({"Questions": self.db})

    def get_specific_question(self, username, questionId):
        results = self.check_database(username, questionId)
        userFound, position,  imHere = results

        if not userFound:
            return jsonify({"Err": "User not found. Please check your username"}), 404

        elif userFound:
            if not imHere:
                return jsonify({"Err": "Question not found. Please check the question Id"}), 404

        return jsonify({"Success": self.db[position][username][int(questionId)]}), 200

    def post_question(self, title, body, username, questionId):
        results = self.check_database(username, questionId)
        userFound, position,  imHere = results

        finalquestion = {
            "title": title,
            "body": body
        }

        brandNew = {
            username: {
                int(questionId): finalquestion
            }
        }

        if not userFound:
            self.db.append(brandNew)
            return jsonify({"Success": self.db[-1][username][int(questionId)]}), 201

        elif userFound:
            if imHere:
                return jsonify({"Err": "Question already exists."}), 400

            elif not imHere:
                self.db[position][username] = {int(questionId): finalquestion}

        return jsonify({"Success": self.db[position][username][int(questionId)]}), 201

    def deleteQuestion(self, username, questionId):
        results = self.check_database(username, questionId)
        userFound, position,  imHere = results

        if not userFound:
            return jsonify({"Err": "This User is not found. Please check your username."}), 404

        elif userFound:
            if imHere:
                del self.db[position][username][int(questionId)]
                return jsonify({"Success": "This question has been deleted."})

            elif not imHere:
                return jsonify({"Err": "This question is not found. It might have been deleted already"}), 404
