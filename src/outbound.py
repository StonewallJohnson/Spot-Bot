import requests

bot_id = "112476b171da9af14a7513ce1a"

def sendChat(message):
    body = {
        "bot_id" : bot_id,
        "text" : message,
    }
    response = requests.post("https://api.groupme.com/v3/bots/post", json=body)    
