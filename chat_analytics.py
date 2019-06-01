### Faceboot Chat Analytics ###
# Python script to gather data from Facebook messenger chats
# Messenger data is given in JSON format


####################### Next steps ########################
# Color coordinate the message data                       #
# Make ranks of most used words per person and altogether #
# Add sentiment analysis to develop profiles              #
# Handle images, videos, etc                              #
###########################################################


################################### Stretch Goals #################################
# Train ML models for each profile and then have them communicate with each other #
###################################################################################


# Import dependencies
from collections import defaultdict
from collections import Counter
import json
import datetime
import time
from itertools import groupby
import matplotlib.pyplot as plt

# Initialize lists
members = []
messages = defaultdict(list)
messageTime = defaultdict(list)
messageTimeUNIX = defaultdict(list)

# Create members list and extract messages
with open('SWAGMA/message_1.json') as json_file:  
    data = json.load(json_file)
    for p in data['participants']:
        members.append(p['name'])
    for p in data['messages']:
        timestamp = datetime.datetime.fromtimestamp(p['timestamp_ms']/1000)
        try:
            messages[p['sender_name']].append(p['content'])
            messageTime[timestamp].extend((p['sender_name'], p['content']))
            messageTimeUNIX[p['timestamp_ms']].extend((p['sender_name'], p['content'])) ### Unix timestamp
        except KeyError: pass

# Find the amount of messages each person has said
mem0 = len(messages[members[0]])
mem1 = len(messages[members[1]])
mem2 = len(messages[members[2]])
mem3 = len(messages[members[3]])
mem4 = len(messages[members[4]])

# Find the total number of messages sent
total = mem0 + mem1 + mem2 + mem3 + mem4

# Find how long chat has been active
currentTime = datetime.datetime.utcnow()
startTime = datetime.datetime.fromtimestamp(min(messageTimeUNIX.keys()) / 1000)
print(startTime)
print(currentTime - startTime)

# Print all the analytics
print("%s has sent %s messages." % (members[0], mem0))
print("%s has sent %s messages." % (members[1], mem1))
print("%s has sent %s messages." % (members[2], mem2))
print("%s has sent %s messages." % (members[3], mem3))
print("%s has sent %s messages." % (members[4], mem4))
print("%s messages have been sent in SWAGMA" % (total))

# Distribution of when the messages were sent
def segment(currentTime):
    k = currentTime + datetime.timedelta(days =- (currentTime.day % 1))
    return datetime.datetime(k.year, k.month, k.day).strftime("%Y-%m-%d")

g = groupby(sorted(messageTime), key = segment)

# Want a dict that is timeslot/key and the count of messages in that slot
group = {}
count = {}

for key, items in g:
    #print(key)
    group.update( {key: list(items)} )
    #print(len(group[key]))
    count.update( {key: len(group[key])})
    #for item in items:
    #    print("|-> %s" % item)

countSorted = sorted(count.items())

# Plot
plt.bar(range(len(countSorted)), list(count.values()), align='center', color = "blue")
plt.xticks(range(len(countSorted)), list(count.keys()))
plt.show()

# Sort messages from timestamp
#for key in sorted(messageTime.keys()):
#    print("%s: %s" % (key, messageTime[key]))