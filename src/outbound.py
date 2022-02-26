import requests
import apiserver
import logging

def sendChat(message):
    body = {
        "bot_id" : apiserver.bot_id,
        "text" : message,
    }
    #logging.info(body);
    response = requests.post("https://api.groupme.com/v3/bots/post", json=body)