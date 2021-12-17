from profile import Profile
import outbound
import logging
logging.basicConfig(filename="../log.txt", level=logging.INFO)

#Maps from user_id and name to profiles
__ids = dict()
__aliases = dict()


#Adds a new profile for the GroupMe member to the id and alias dicts
def registerMember(id, alias):
    newMember = Profile(id, alias)
    __ids[id] = newMember
    __aliases[alias] = newMember
    logging.info("Registered a new member, ID: "+ id +", alias: "+ alias)
    outbound.sendChat("Registered: "+alias+". Welcome!")
