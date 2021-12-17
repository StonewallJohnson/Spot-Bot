from flask import Flask
from flask_restful import Resource, Api, reqparse
import utility
import json

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
        dict = json.loads(str(argDict).replace("'", "\""))
        print(type(dict), dict)
        print(type(argDict), argDict)

        mentions = utility.getMentionsFromAttachments(argDict["attachments"])
        text = argDict["text"]
        #look for any command escapes ('!<>') in text
        if text.find("!register") != -1:
            utility.registerMember(argDict["sender_id"], argDict["name"])
        
        if text.find("!members") != -1:
            utility.showMembers()
        
        if text.find("!unregister") != -1:
            utility.unregisterMember(argDict["sender_id"], argDict["name"])
        
        spotted = text.find("Spotted") != -1 or text.find("spotted") != -1
        tagged = len(mentions) != 0
        if spotted and tagged:
            utility.spot(argDict["sender_id"], mentions)  

        return argDict, 200


api.add_resource(ChatEndpoint, "/chat")

if __name__ == '__main__':
    open("../log.txt", "w").close()
    app.run(port=50000)