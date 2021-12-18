from profile import Profile
import outbound
import logging
from operator import itemgetter
logging.basicConfig(filename="../log.txt", level=logging.INFO)

#Maps from user_id and name to profiles
__profiles = dict()
usageScript = """Commands '!<>':\n
usage: shows what each command does\n
register: starts tracking when the sender is spotted or spots\n
unregister: stops tracking when the sender is spotted or spots and removes all counts of spotting or being spotted\n
members: shows who is registered\n
leaderboard: shows registered members in descending order by spots\n
\n
Spotting:\n
In order to properly spot someone, the word 'Spotted' or 'spotted'
must present in the message and those who are spotted must be @.\n
Both the spotter and the spotted must be registered in order for the spot to
appear on the leaderboard.
"""
#Adds a new profile for the GroupMe member to the id and alias dicts
def registerMember(id, alias):
    newMember = Profile(id, alias)
    __profiles[id] = newMember
    outbound.sendChat("Registered: "+alias+". Welcome!")
    logging.info("Registered a new member, ID: "+ id +", alias: "+ alias)

#TODO: look to see if string concatenation is recreating the string
#Will send a message to the chat with all registered members
def showMembers():
    message = "Registered Members:\n"
    for id in __profiles:
        #for every person in the __ids dict
        message += __profiles[id].alias + "\n"
    outbound.sendChat(message)
    logging.info("Printed the registered members.")

def unregisterMember(id, alias):
    __profiles.pop(id)
    outbound.sendChat("Unregistered: "+alias)
    logging.info("Unregistered a member, ID: "+ id +", alias: "+ alias)

def spot(spotterID, spottedIDs):
    spotter = __profiles[spotterID]
    if spotter != None:
        for spottedID in spottedIDs:
            spotted = __profiles[spottedID]
            if spotted != None:
                spotter.spottedSomeone()
                spotted.gotSpotted()
                logging.info(spotter.alias+" spotted "+spotted.alias)
        
def showLeaderboard():
    message = "Leaderboard\n"
    #sort keys into descending order based on spots belonging to that key
    orderedKeys = sorted(__profiles, key=getter, reverse=True)
    
    for key in orderedKeys:
        #for every key, append the representation of that key
        message += repr(__profiles[key]) + "\n"
    
    outbound.sendChat(message)
    logging.info("Printed leaderboard")

def getter(key):
    return __profiles[key].spots

def printUsage():
    outbound.sendChat(usageScript)

def changeName(text :str):
    partition = text.partition(" changed name to ")
    old = partition[0]
    new = partition[2]
    for key in __profiles:
        if __profiles[key].alias == old:
            __profiles[key].changeAlias(new)
            logging.info("Change alias: '" +old+"' to: '"+new+"'")    

def getMentionsFromAttachments(attachments):
    for element in attachments:
        if element["type"] == "mentions":
            return element["user_ids"] 