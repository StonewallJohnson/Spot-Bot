import requests
import utility

MAX_MESSAGE_SIZE = 600

def sendChat(message):
    messageLen = len(message)
    sentChars = 0
    while sentChars < messageLen:
        #this loop divides the message into chunks that are sized according to
        #MAX_MESSAGE_SIZE. This means that messages over the MAX_MESSAGE_SIZE
        #will be sent as multiple messages 
        #using integer division: 
        #(messageLen / MAX_MESSAGE_SIZE) + 1
        messageChunk = message[sentChars:sentChars + MAX_MESSAGE_SIZE]
        body = {
            "bot_id" : utility.BOT_ID,
            "text" : messageChunk,
        }
        response = requests.post("https://api.groupme.com/v3/bots/post", json=body)
        sentChars += len(messageChunk)
