from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from marshmallow import Schema, fields
import utility

#Flask wizardry
app = Flask(__name__)
api = Api(app)

class ChatEndpoint(Resource):
    def post(self):
        #Retrieve JSON sent with the post
        message_json = request.get_json()
        #Compose JSON into a marshmallow schema
        MessageSchema = Schema.from_dict(message_json)

        mentions = utility.getMentionsFromAttachments(MessageSchema.attachments)
        text = MessageSchema.text

        #look for any command escapes ('!<>') in text
        if text.find("!register") != -1:
            utility.registerMember(MessageSchema.sender_id, MessageSchema.name)
        
        if text.find("!members") != -1:
            utility.showMembers()
        
        if text.find("!unregister") != -1:
            utility.unregisterMember(MessageSchema.sender_id, MessageSchema.name)
        
        if someoneSpotted(text, mentions):
            utility.spot(MessageSchema.sender_id, mentions)

        if text.find("!leaderboard") != -1:
            utility.showLeaderboard() 
    
        return "returned", 200

def someoneSpotted(text, mentions):
    spotted = False
    tagged = False
    spotted = text.find("Spotted") != -1 or text.find("spotted") != -1
    if mentions and len(mentions) != 0:
            tagged = True
    return spotted and tagged


api.add_resource(ChatEndpoint, "/chat")

if __name__ == '__main__':
    open("../log.txt", "w").close()
    app.run(port=50000)