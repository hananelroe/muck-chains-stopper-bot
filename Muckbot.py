# this bot was made by u/hananelroe on reddit
import collections
import warnings
warnings.filterwarnings('ignore', '.*slow pure-python SequenceMatcher.*')
import thefuzz.fuzz as fuzz
import praw
import unicodedata
import random
import sys
from threading import Thread
import datetime
import pytz
import schedule
import json
from colors import color
import console


# details about the bot to send after every comment
credit = "\n______\n ^(I'm just a simple bot that wants to stop muck chains, [here is my github page](https://github.com/hananelroe/muck-chains-stopper-bot)\
, you can see my source code and submit my issues there)\n\n ^(I'm a collaboration between [Hananelroe](https://www.reddit.com/u/Hananelroe) and [HoseanRC]\
(https://www.reddit.com/u/HoseanRC))\n\n^([visit my website](https://www.reddit.com/r/Damnthatsinteresting/comments/ovp6t1/never_gonna_give_you_up_by_rick_astley_remastered))"

shut = "#**SHUT**"  # shut comment for m***
bad_bot = "WHY?"  # WHY? comment for "bad bot"
good_bot = "thanks! :)"  # thanks comment for "good bot"

fixed_comment = ""  # fixing comments to get better muck results

unwanted_characters = [" ", ",", ".", "\n", "\'"]

mucks_Counter = 0
yesterday_Mucks = 0
mucks_count_content1 = "**you have summoned me to show you the state of this sub**\n\ntoday I have counted **"  # the Asterisks are for bolding the counters' numbers
mucks_count_content2 = "** mucks.\n\nyesterday I have counted **"
mucks_count_disclaimer = "^(I don't reply to all mucks, but I do count both mucks that are a part of a chain and mucks that aren't, and the count resets every day.) \n\n^(if you've noticed a problem or want to contribute to my code, [here is my GitHub page](https://github.com/hananelroe/muck-chains-stopper-bot))"

consoleMode = False

preferencesFile = open("preferences.json", "r+")
preferences = json.load(preferencesFile)

class author:
    def __init__(self):
        self.name = None

class EmptyComment:  # Empty comment class for parent function
    def __init__(self):
        # fake attributes:
        self.body = None
        self.author = author()
        self.author.name = None


def parent(child_comment):  # gets comment's parent (aka the comment it replied to)
    # and returns a fake empty comment if it didn't find one

    parent_comment = EmptyComment()  # create empty object for the fake comment
    parent_comment.author = EmptyComment()  # add empty object for name for the author of the fake comment
    parent_comment.author.name = ""  # add the fake comment's author name
    try:
        if str(type(
                child_comment.parent())) == "<class 'praw.models.reddit.comment.Comment'>":  # check if it's a comment
            parent_comment = child_comment.parent()  # if it did find the comment, it will
            # save it, otherwise it will raise error
    finally:
        return parent_comment  # at the end returns the same output as comment.parent()
        # but it will return empty comment instead of any error


def noglyph(s):  # removes any glyph from a character (ex. ý -> y, Ŕ -> R)
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def printComment(comment, fixed_comment, authorName):
    if authorName != preferences["username"]:
        print(color.PURPLE + comment + " "  # prints the original comment, the fixed one,
              + color.BLUE + fixed_comment  # and the fixed comment similarity to "muck"
              + f" {color.END}" + str(fuzz.ratio(fixed_comment, "muck")) + "%"
              + f"\nu/{color.CYAN}{authorName}{color.END}\n")


def reply(comment, content, credit):  # replies with/without credit according to the chain's length
    try:
        # check if the comment have more than 4 parents:
        comment.parent().parent().parent().parent()
    except:
        # if the comment does have more than 4 parents:
        comment.reply(content + credit)
    else:
        comment.reply(content)  # else than comment bad_bot without credit


def resetMuckCount():
    global yesterday_Mucks, mucks_Counter
    yesterday_Mucks = mucks_Counter
    mucks_Counter = 0
    print("resetting muck count...")


def getUTCMidnight():
    final = ""
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    a = pytz.utc.localize(datetime.datetime(1, 1, 1, 0, 0)).astimezone(local_tz)

    if a.hour < 10:
        final = final + "0" + str(a.hour)
    else:
        final = a.hour
    if a.minute < 10:
        final = final + ":0" + str(a.minute)
    else:
        final = final + ":" + str(a.minute)
    return final


def savePreferences(file, data):
    file.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, file, indent=4)
    file.truncate()  # remove remaining part


def main():
    global fixed_comment, mucks, mucks_Counter, yesterday_Mucks, consoleMode, preferences

    # for every new comment:
    for comment in subreddit.stream.comments(skip_existing=True):
        if consoleMode:
            break  # we shouldn't run the bot when using the console

        fixed_comment = comment.body.lower()

        # removing unwanted characters:
        for character in unwanted_characters:
            fixed_comment = fixed_comment.replace(character, "")

        # removing glyphs:
        fixed_comment = noglyph("".join(dict.fromkeys(fixed_comment)))

        # print comment details:
        printComment(comment.body, fixed_comment, comment.author.name)

        # skip the comment check if the commenter is the bot or the user is blocked:
        if comment.author.name == preferences["username"]:
            continue
        if comment.author.name.lower() in preferences["blocked users"]:
            print(f"{color.RED}USER BLOCKED{color.END}")
            continue

        # when someone mentions the bot:
        if comment.body.lower() == f"u/{preferences['username'].lower()}":
            if int(yesterday_Mucks) < int(mucks_Counter):  # if today there were more mucks than yesterday:
                print(f"{color.CYAN}someone mentioned me! {color.RED}and it gets worse...{color.END}")
                comment.reply(mucks_count_content1 + str(mucks_Counter) + mucks_count_content2 + str(
                    yesterday_Mucks) + "** mucks. it gets worse...\n\n" + mucks_count_disclaimer)
            else:
                print(f"{color.CYAN} someone mentioned me! {color.GREEN}and it gets better!{color.END}")
                comment.reply(mucks_count_content1 + str(mucks_Counter) + mucks_count_content2 + str(
                    yesterday_Mucks) + "** mucks. we're getting better!\n\n" + mucks_count_disclaimer)

        # if the comment replied to the bot:
        if parent(comment).author.name == preferences["username"]:
            if comment.body.lower() == "bad bot:":
                print(f"{color.GREEN} bad bot MATCH! replying...{color.END}\n")
                reply(comment, bad_bot, credit)
            elif comment.body.lower() == "good bot":
                print(f"{color.GREEN}good bot MATCH! replying...{color.END}")
                reply(comment, good_bot, credit)
        else:
            for item in preferences["muck list"]:
                # if the comment is >74% "muck" and starts/ends with "m"/"k":
                if fuzz.ratio(fixed_comment, item) > 74 and fixed_comment[0] in "mk":
                    if preferences["reduce comments"]:
                        if random.randrange(1, 5) == 1:  # roughly 1 out of 5 comments:
                            print(f"{color.GREEN}MUCK detected! replying...{color.END}\n")
                            reply(comment, shut, credit)
                            mucks_Counter += 1
                        else:
                            print(f"{color.RED}MUCK detected! not replying{color.END}\n")
                        break
                    else:
                        print(f"{color.GREEN}MUCK detected! replying...{color.END}\n")
                        reply(comment, shut, credit)
                        mucks_Counter += 1
                    break
            continue


def consoleFunc():
    global consoleMode, preferencesFile
    while True:
        if input() == "console" and consoleMode == False:
            print("\n" * 100)  # to clear all other outputs
            print(f"{color.PURPLE}console mode{color.END}")
            preferencesFile.close()
            consoleMode = True
        if consoleMode:
            while True:
                command = input()
                if command == "quit":
                    preferencesFile = open("preferences.json", "r+")
                    print(f"{color.PURPLE}quitting console{color.END}")
                    consoleMode = False
                    break
                else:
                    console.main(command)


def dailyRoutine():
    schedule.every().day.at(getUTCMidnight()).do(resetMuckCount, )
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    # creating an authorized reddit instance from the given data
    reddit = praw.Reddit(client_id=preferences["client ID"],
                         client_secret=preferences["client secret"],
                         username=preferences["username"],
                         password=preferences["password"],
                         user_agent=preferences["user agent"])

    # selects the subreddit to read the comments from
    subreddit = reddit.subreddit(preferences["subreddit name"])
    print(f"{color.GREEN}online{color.END}")

    try:
        mainThread = Thread(target=main)
        routineThread = Thread(target=dailyRoutine)
        '''consoleTread = Thread(target=consoleFunc)'''  # the console doesn't really work, I might fix it in the future

        mainThread.start()
        routineThread.start()
        '''consoleTread.start()'''

    except KeyboardInterrupt:  # Ctrl-C - stop
        savePreferences(preferencesFile, preferences)
        preferencesFile.close()
        print(f"{color.RED}Bye!{color.END}")

    except Exception as error:  # Any exception
        savePreferences(preferencesFile, preferences)
        preferencesFile.close()
        print(
            f"{color.RED}Error in line {sys.exc_info()[-1].tb_lineno}: {error}")  # prints error line and the error itself
        print(f"Trying to restart...{color.END}")
