from profile import Profile
import outbound
import logging
logging.basicConfig(level=logging.INFO)



##Reads the profiles from the backup file and updates the __profiles map
#Maps from user_id and name to profiles
__profiles = dict()
BACKUP_FILE_PATH = "aux_file/backup.txt"
BOT_ID = ""

usageScript = """2Q]Z&tQaF(NsZ5e@`$fk)v%&#VP=I8
\=J#6{5cm\Y[|fAsc%'n9A%8<;dkP 
x^`JD7*&B$Md(t&p~t{L:{[9TRlH4,
%y:/ i:KtyG}pzwOYjD0 D+aafS)H1
`Iv@4E#{2_WA]S/0l2 _F`(A,e0}W2
!#O/nuZ*C_zjlfW:$J8'Z9qhoFB6|)
Le^ 4ch%o${VqYu$U/;0;<Kst]j!.E
ZQ{>3`Qty_<%Q;,}m&~> 1mS):&a B
_tA.fm@5 $SAR@ATLz=o2vRbJ%YgIl
$5mN|$[XtOSV'zO$rIZtoWL$E_5Nr!
I$1Cn ]A,gNjMJ626bv#8H$<9e&ca#
(,tEKJs2o<u.Z+;{g6M?B:&qHME"GC
I.dXKT3%~ve5?P5a{C-1Fm+"@fY4k-
,EraLN@g@GK:~i_$>h,N@~w5>Vy[,L
?l _/;J+k,[L!%Zydt5$}N(8( OL7)
h-SkS~%r;zePL&tHH[nG*K boK%p0O
"q&&U/V@zVsN`UfO'#+B54SSfQpy1B
MuQo[&ME/w}X8`MjvAhFJi^'a]|2!W
orhsSU-=sc82-=#zo"?}bIWhUbUeh>
S!"'#N%^/0:=M*=B0p9a9j$^86jD0B
-pi/9;U<yiRkJmwX,)'I6(?6BK}6tg
FKFz\BMKP0|!wLQre8n,gaIUxLeHdX
lAejRkqnNBV)-!/9M$@5j2'q -;V'X
gvWJH5i,<<l=GB4}&G%Fv}rqkdj*sT
lI}XQe}eh)]2kCZJ<K\dz3Go<lj.gH
D;5o;p3J"Y`@@B@{%v^v`&;C?G9>"E
8bqN:4?%j?:B/bQfc3)!}!A7,p{27^
6h%D<07v4e1a>^T5P9c2[zPD*4tffh
7fK?x\*5*k;N21jv6{ !8$cQVL+^h:
W'IiZF!$U1%Zy5qMQAFL6?PM7R~SB~
aSS*R\hhlbk8;HoG|nL }W>n?lu&7=
juG%n|vxYFD;@5G<.Gr$SvtEXE;:1H
FMbznV|zMD*H}24S}mnLsh%PP]G$1J
Pmr=qpht5KYRk< PR{Z&B.5{ Y[Wdp
WzPe'3gR*:@rgzD`*0OzVa_6.E5=dq
S}JlU8<M6qOA,qd#d;ccr(@$TBrs[v
~iQq01g19rFr_zc6|D_2`8td #JN[h
bX47CuuQ9b(t7~>d`+fQ8XT5x=)M-A
;hdZr$]dVLgtcK!s2M.Z(Cc$d-%(_T
iiBV;s0X:1,x ^A>9$nduUieq+)+1f"""

#Adds a new profile for the GroupMe member to the id and alias dicts
def registerMember(id, alias, spotted = 0, spots = 0):
    if id not in __profiles.keys():
        newMember = Profile(id, alias, spotted, spots)
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
    orderedKeys = sorted(__profiles, key=spotsGetter, reverse=True)
    
    for key in orderedKeys:
        #for every key, append the leaderboard info of that key
        message += __profiles[key].leaderboardInfo() + "\n"
    
    outbound.sendChat(message)
    logging.info("Printed leaderboard")

def showStreaks():
    message = "Streaks\n"
    #sort keys into descending order based on spots belonging to that key
    orderedKeys = sorted(__profiles, key=streakGetter, reverse=True)
    
    for key in orderedKeys:
        #for every key, append the streak info of that key
        message += __profiles[key].streakInfo() + "\n"
    
    outbound.sendChat(message)
    logging.info("Printed streaks")

def spotsGetter(key):
    return __profiles[key].spots

def streakGetter(key):
    return __profiles[key].spotStreak

def netGetter(key):
    return __profiles[key].getNetSpots()

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


def declareWinner():
    orderedKeys = sorted(__profiles, key=netGetter, reverse=True)
    winner = __profiles[orderedKeys[0]]
    message = """The winner, by net spots is... {}
    with {} net spots.
    
    Congratulations! Here is what the leaderboard looked like:""".format(winner.alias, winner.getNetSpots())
    outbound.sendChat(message)
    showLeaderboard()

def erase():
    __profiles = dict()
    writeBackup()

def restoreFromBackup():
    print("Restoring from " + BACKUP_FILE_PATH)
    file = open(BACKUP_FILE_PATH)
    info = file.readline().strip()
    
    while(info):
        #for each person backed up, make profile and map
        vars = info.split("\t")
        newMember = Profile(vars[0], vars[1], int(vars[2]), int(vars[3]))
        __profiles[vars[0]] = newMember
        info = file.readline().strip()
    file.close()

def writeBackup():
    file = open(BACKUP_FILE_PATH, "w")
    for key in __profiles:
        #for every registered member
        delimiter = '\t'
        str = ""
        prof = __profiles[key]
        str += prof.id + delimiter
        str += prof.alias + delimiter
        str += repr(prof.spotted) + delimiter
        str += repr(prof.spots) + "\n"
        file.write(str)
    file.close()


