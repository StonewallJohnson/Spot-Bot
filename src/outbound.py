import sys
import requests

bot_id = sys.argv[1]

def sendChat(message):
    body = {
        "bot_id" : bot_id,
        "text" : message,
    }
    response = requests.post("https://api.groupme.com/v3/bots/post", json=body)