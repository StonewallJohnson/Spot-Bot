import requests
import apiserver

def sendChat(message):
    body = {
        "bot_id" : apiserver.bot_id,
        "text" : message,
    }
    response = requests.post("https://api.groupme.com/v3/bots/post", json=body)