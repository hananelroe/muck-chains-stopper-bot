import os
import json
import muckbot
from colors import color

blockedUser = ""
preferencesFile = open("preferences.json", "r+")

def saveJSON(file, data):
    file.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, file, indent=4)
    file.truncate()  # remove remaining part

def blockUser(user):
    a = json.load(preferencesFile)
    a["blocked users"].append(str(user).lower())
    saveJSON(preferencesFile, a)

def unblockUser(user):
    a = json.load(preferencesFile)
    a["blocked users"].remove(str(user).lower())
    saveJSON(preferencesFile, a)


commandsMap = {
        "quit" : ["",                # command output
                  "quits console"],  # command description
        "print mucks": [f"mucks counted today: {muckbot.mucks_Counter}\nmucks counted yesterday: {muckbot.yesterday_Mucks}",
                        "prints the muck counted today and yesterday"],
        "block": [f"{color.RED}enter user name to block{color.END}",
                       "blocks a given user"],
        "unblock": [f"{color.GREEN}enter user name to unblock{color.END}",
                         "unblocks a given user"]
           }

def main(command):
    if command == "help":
        for i in commandsMap.keys():
            print(f"\"{str(i)}\" - {commandsMap[i][1]}")
    else:
        if command in commandsMap:
            print(commandsMap[command][0])
            if command == list(commandsMap)[2]:  # block user
                user = input()
                blockUser(user)
                print(f"{color.RED}\"{user}\" was added to blacklist{color.END}")
            elif command == list(commandsMap)[3]:  # unblock user
                user = input()
                try:
                    unblockUser(user)
                    print(f"{color.GREEN}\"{user}\" was removed from blacklist{color.END}")
                except:
                    print(f"{color.RED}\"{user}\" wasn't found inside the blacklist")
