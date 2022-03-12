import requests
import apiserver
import utility

def sendChat(message):
    body = {
        "bot_id" : utility.BOT_ID,
        "text" : message,
    }
    print(type(utility.BOT_ID))
    print("trying to post to bot id: " + utility.BOT_ID)
    response = requests.post("https://api.groupme.com/v3/bots/post", json=body)