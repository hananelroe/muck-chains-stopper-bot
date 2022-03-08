import os
import json
import muckbot
from colors import color

blockedUser = ""
preferences = None  # this one gets updated when we call the console from muckbot.py


def not_a_func():
    pass


def blockUser():
    global preferences
    user = input()
    preferences["blocked users"].append(str(user).lower())
    print(f"{user} was added to the blacklist")


def unblockUser():
    global preferences
    user = input()
    try:
        preferences["blocked users"].remove(str(user).lower())
    except:
        print(f"{color.RED}\"{user}\" wasn't found in the blacklist{color.END}")


commandsMap = {
    "quit": ["",  # command output
             "quits console",  # command description
             not_a_func],  # command function
    "print counters": [f"\"muck\":\ntoday: {muckbot.mucks_Counter}, yesterday: {muckbot.yesterday_Mucks}\n\n"
                       f"\"wow that was really cool\":\ntoday: {muckbot.wowThatWasReallyCoolCount}, yesterday: {muckbot.yesterday_WowThatWasReallyCool}\n",
                       "prints today\'s and yesterday\'s counters",
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
        else:
            print(
                f"{color.RED}\"{command}\" wasn't recognised as a command. check for spelling errors "
                f"or type \"help\" for commands list.{color.END}")
