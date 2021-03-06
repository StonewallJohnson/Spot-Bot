from flask import Flask, request
from flask_restful import Resource, Api
from marshmallow import Schema
import argparse
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
            
        if text.find("!streaks") != -1:
            utility.showStreaks()

        return "returned", 200

class ControlEndpoint(Resource):
    def get(self):
        return """Send me a post request that looks like:
        {
            "control_action" : <int>
        }
        control_action:
            0: backup
            1: server check
            2: declare a winner
            5: erase all data
        """, 200

    def post(self):
        #Retrieve JSON sent with the post
        message_json = request.get_json()
        #Compose JSON into a marshmallow schema
        MessageSchema = Schema.from_dict(message_json)
        if MessageSchema.control_action == 0:
            utility.writeBackup()
            return "Backed up profiles", 200
        
        if MessageSchema.control_action == 1:
            return "server is alive", 200

        if MessageSchema.control_action == 2:
            utility.declareWinner()
            return "Winner declared", 200

        if MessageSchema.control_action == 5:
            utility.erase()
            return "Members wiped and no backup", 200

        return "Could not recognize request", 400

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
api.add_resource(ControlEndpoint, "/control")

##ENTRYPOINT
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Starts the server that posts to a given bot id.")
    parser.add_argument("bot_id")
    parser.add_argument("--fromBackup", action="store_true")
        
    namespace = parser.parse_args()
    argsDict = vars(namespace)

    utility.BOT_ID = namespace.bot_id
    if namespace.fromBackup:
        utility.restoreFromBackup()

    app.run(host="0.0.0.0", port=50000)