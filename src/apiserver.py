from flask import Flask
from flask_restful import Resource, Api, reqparse
import utility

#Flask wizardry
app = Flask(__name__)
api = Api(app)

class ChatEndpoint(Resource):
    def post(self):
        #Parse JSON from chat
        parser = reqparse.RequestParser()
        parser.add_argument("sender_id")
        parser.add_argument("name")
        parser.add_argument("text")
        parser.add_argument("attachments") 
        argDict = parser.parse_args()


        text = argDict["text"]
        #look for any command escapes ('!<>') in text
        if text.find("!register") != -1:
            utility.registerMember(argDict["sender_id"], argDict["name"])

        return argDict, 200


api.add_resource(ChatEndpoint, "/chat")

if __name__ == '__main__':
    open("../log.txt", "w").close()
    app.run(port=50000)