from flask import Flask, request, jsonify

from .. import version1


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


@version1.route("/questions", methods=["POST"])
def postQuestion():
    """ Posts a question """
    userFound, imHere = False, False
    position = 0
    title = request.get_json()["title"]
    body = request.get_json()["body"]
    questionId = request.get_json()["questionId"]
    userName = request.get_json()["uname"]

    finalquestion = {
        "title": title,
        "body": body
    }

    brandNew = {
        userName: {
            int(questionId): finalquestion
        }
    }

    for user in range(len(questions)):
        for key, value in questions[user].items():
            if key == userName:
                userFound = True
                position = user
                for question in value.keys():
                    if question == int(questionId):
                        imHere = True
                        break

    if not userFound:
        questions.append(brandNew)
        return jsonify(questions[-1][userName][int(questionId)])

    elif userFound:
        if imHere:
            return jsonify({"Err": "Question already exists."}), 400
        elif not imHere:
            questions[position][userName] = {int(questionId): finalquestion}

    return questions[position][userName][int(questionId)]
