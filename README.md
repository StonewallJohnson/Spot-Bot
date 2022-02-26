# Spot Bot
This repository contains the API code for a GroupMe bot. This API allows the GroupMe bot to send the messages of the chat to,
reads the messages, then looks for any command sequences or spots and keeps track of who spots or gets spotted. 

# Usage
### Commands '!<>':
**usage**: shows what each command does

**register**: starts tracking when the sender is spotted or spots

**unregister**: stops tracking when the sender is spotted or spots and removes all counts of spotting or being spotted

**members**: shows who is registered

**leaderboard**: shows registered members in descending order by spots

### Spotting:
In order to properly spot someone, the word 'Spotted' or 'spotted'
must be present in the message and those who are spotted must be @.
Both the spotter and the spotted must be registered in order for the spot to appear on the leaderboard.

# Startup
python apiserver.py *GroupMe bot_id* *Optional: relative backup file path* 