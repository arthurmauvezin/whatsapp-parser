import re
import datetime
import emoji
import pytz
from google.cloud import firestore
import sys

path = f"./{str(sys.argv[1])}"

timezone = pytz.timezone("Europe/Paris")

entries = []
with open(path, "r") as fp:
    for line in fp:
        regex_entry = re.match(r"(\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2} [A|P]M) - ([\w\s]+): (.+)", line)

        if regex_entry:
            entry = {}
            date = datetime.datetime.strptime(regex_entry.group(1), "%m/%d/%y, %I:%M %p")
            entry["date"] = timezone.localize(date)
            entry["user"] = regex_entry.group(2)
            entry["message"] = regex_entry.group(3)
            entries.append(entry)
        else:
            regex_entry = re.match(r"(\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2} [A|P]M) - (.+)", line)
            if regex_entry:
                entry = {}
                date = datetime.datetime.strptime(regex_entry.group(1), "%m/%d/%y, %I:%M %p")
                entry["date"] = timezone.localize(date)
                entry["user"] = "whatsapp_system"
                entry["message"] = regex_entry.group(2)
                entries.append(entry)
            else:
                line = line.rstrip("\n")
                entries[-1]["message"] += f"\n{line}"


db = firestore.Client()


def setfsdoc(document):
    new_doc = db.collection('groups').document('bfmtv').collection('entries').document()
    new_doc.set(document)


# Add meta informations
for entry in entries:
    message = entry["message"]
    entry["number_emoji"] = emoji.emoji_count(message)
    entry["number_word"] = len(message.split())
    entry["number_char"] = len(message)

# print(json.dumps(entries))

for entry in entries:
    setfsdoc(entry)
