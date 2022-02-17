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

def not_a_func():
    pass

def blockUser():
    user = input()
    a = json.load(preferencesFile)
    a["blocked users"].append(str(user).lower())
    saveJSON(preferencesFile, a)
    print(f"{user} was added to the blacklist")

def unblockUser():
    user = input()
    a = json.load(preferencesFile)
    try:
        a["blocked users"].remove(str(user).lower())
        saveJSON(preferencesFile, a)
    except:
        print(f"{color.RED}\"{user}\" wasn't fount in the blacklist{color.END}")


commandsMap = {
        "quit": ["",               # command output
                 "quits console",  # command description
                 not_a_func],      # command function
        "print mucks": [f"mucks counted today: {muckbot.mucks_Counter}\nmucks counted yesterday: {muckbot.yesterday_Mucks}",
                        "prints the muck counted today and yesterday",
                        not_a_func],
        "block": [f"{color.RED}enter user name to block{color.END}\n(without u/)",
                  "blocks a given user",
                  blockUser
                  ],
        "unblock": [f"{color.GREEN}enter user name to unblock{color.END}\n(without u/)",
                    "unblocks a given user",
                    unblockUser]
           }

def main(command):
    if command == "help":
        for i in commandsMap.keys():
            print(f"\"{str(i)}\" - {commandsMap[i][1]}")
    else:
        if command in commandsMap:
            print(commandsMap[command][0])
            commandsMap[command][2]()
