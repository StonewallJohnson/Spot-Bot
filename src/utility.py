from profile import Profile
import outbound
import logging
import json
logging.basicConfig(filename="../log.txt", level=logging.INFO)

#Maps from user_id and name to profiles
__ids = dict()
__aliases = dict()


#Adds a new profile for the GroupMe member to the id and alias dicts
def registerMember(id, alias):
    newMember = Profile(id, alias)
    __ids[id] = newMember
    __aliases[alias] = newMember
    outbound.sendChat("Registered: "+alias+". Welcome!")
    logging.info("Registered a new member, ID: "+ id +", alias: "+ alias)


#Will send a message to the chat with all registered members
def showMembers():
    message = "Registered Members:\n"
    for id in __ids:
        #for every person in the __ids dict
        message += __ids[id].alias + "\n"
    outbound.sendChat(message)
    logging.info("Printed the registered members.")

def unregisterMember(id, alias):
    __ids.pop(id)
    __aliases.pop(alias)
    outbound.sendChat("Unregistered: "+alias)

def spot(spotterID, spottedIDs):
    spotter = __ids[spotterID]
    if spotter != None:
        for spottedID in spottedIDs:
            spotted = __ids[spottedID]
            if spotted != None:
                spotter.spottedSomeone()
                spotted.gotSpotted()
                logging.info(spotter.alias+" spotted "+spotted.alias)
        


def getMentionsFromAttachments(attachments: str):
    new = attachments.replace("'", "\"")
    data = json.loads(new)
    print(type(data), data)
    
    if data["type"] == "mentions":
        return data["user_ids"] 