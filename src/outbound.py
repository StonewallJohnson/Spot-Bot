import requests
import apiserver
import utility

def sendChat(message):
    messageLen = len(message)
    print("Message size: ", messageLen)
    sentChars = 0
    while sentChars < messageLen:
        chunk = message[sentChars:sentChars + 400]
        sentChars += 400
        print("Chunk size: ", len(chunk))
        body = {
            "bot_id" : utility.BOT_ID,
            "text" : chunk,
        }
        print(type(utility.BOT_ID))
        print("trying to post to bot id: " + utility.BOT_ID)
        response = requests.post("https://api.groupme.com/v3/bots/post", json=body)
        print(response)