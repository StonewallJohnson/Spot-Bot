import requests
import utility

def sendChat(message):
    body = {
        "bot_id" : utility.BOT_ID,
        "text" : message,
    }
    response = requests.post("https://api.groupme.com/v3/bots/post", json=body)
