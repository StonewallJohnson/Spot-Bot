from flask import Flask, request
from flask_restful import Resource, Api
from marshmallow import Schema
import sys
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
        
        if text.find("!usage") != -1:
            utility.printUsage()

        if nameChangeDetected(MessageSchema):
            utility.changeName(MessageSchema.text)
            
        
        return "returned", 200

class BackupEndpoint(Resource):
    def get(self):
        utility.writeBackup()
        return "Backed up profiles", 200

def someoneSpotted(text, mentions):
    spotted = False
    tagged = False
    spotted = text.find("Spotted") != -1 or text.find("spotted") != -1
    if mentions and len(mentions) != 0:
            tagged = True
    return spotted and tagged

def nameChangeDetected(message):
    return message.sender_id == "system" and message.text.find("changed name to") != -1

api.add_resource(ChatEndpoint, "/chat")
api.add_resource(BackupEndpoint, "/back_me_up")

bot_id = None
##ENTRYPOINT
if __name__ == '__main__':
    args = len(sys.argv)
    if args > 3 or args < 2:
        exit("Usage: apiserver.py <bot_id> <OPTIONAL: relative backup file path>")
    
    if sys.argv[1] == None:
        exit("Need a bot id to post to!")
    else:
        bot_id = sys.argv[1]
    
    if args == 3:
        if sys.argv[2] != None:
            utility.restoreFromBackup(sys.argv[2])
        
    app.run(host="0.0.0.0", port=50000)