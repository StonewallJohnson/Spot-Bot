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
        parser.add_argument("text")
        argDict = parser.parse_args()
        
        return argDict, 200


api.add_resource(ChatEndpoint, "/chat")

if __name__ == '__main__':
    app.run(port=50000)