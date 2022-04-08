# this bot was made by u/hananelroe on reddit
# counts muck and "that was really cool" chains
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

# the counter will increase the counter variables instead of replying to comments
thatWasCoolChains = 0
muckCounts = 0
totalComments = 0

# details about the bot to send after every comment
credit = "\n______\n ^(I'm a bot that stops \"muck\" and \"wow that was really cool\" chains)\n\n" \
         "[GitHub](https://github.com/hananelroe/muck-chains-stopper-bot)^([report an issue](https://github.com/hananelroe/muck-chains-stopper-bot/issues/new))\n\n" \
         "^([visit my website](https://www.reddit.com/r/Damnthatsinteresting/comments/ovp6t1/never_gonna_give_you_up_by_rick_astley_remastered))"

shut = "#**SHUT**"  # shut comment for m***
thatWasntCool = "that was cool, but your chain isn\'t."
bad_bot = "WHY?"  # WHY? comment for "bad bot"
good_bot = "thanks! :)"  # thanks comment for "good bot"

consoleMSG = f"{color.PURPLE}console mode\n{color.RED}WARNING: the bot stops working when you are in the console mode." \
             f" to make him work again, quit the console by typing \"quit\"{color.END}"

fixed_comment = ""  # fixing comments to get better muck results

unwanted_characters = [" ", ",", ".", "\n", "\'", "!", "@"]  # the characters in this list will be ignored by the bot

mucks_Counter = 0
yesterday_Mucks = 0
wowThatWasReallyCoolCount = 0
yesterday_WowThatWasReallyCool = 0
consoleMode = False

preferencesFile = open("preferences.json", "r+")
preferences = json.load(preferencesFile)


class author:
    def __init__(self):
        self.name = ""


class EmptyComment:  # Empty comment class for parent function
    def __init__(self):
        # fake attributes:
        self.body = ""
        self.author = author()
        self.author.name = ""


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


def fixComment(comment):
    fixed = comment.body.lower()
    # removing unwanted characters:
    for character in unwanted_characters:
        fixed = fixed.replace(character, "")
    # removing glyphs:
    fixed = noglyph("".join(dict.fromkeys(fixed)))
    return fixed


def printComment(comment, fixed_comment, authorName):
    if authorName != preferences["username"]:
        print(color.PURPLE, comment, color.BLUE, fixed_comment, color.END,  # prints comment, fixed comment,
              f" \"muck\" similarity:",
              color.RED, str(fuzz.ratio(fixed_comment, "muck")), "%", color.END,  # "muck" similarity,
              " \"wow that was really cool\" similarity:",
              color.RED, (fuzz.ratio(fixed_comment, "wothasrelyc")), "%", color.END,
              # "wow that was really cool" similarity
              f"\nu/{color.CYAN}{authorName}{color.END}\n")  # and author name


def savePreferences(file, data):
    file.seek(0)  # <--- should reset file position to the beginning.
    json.dump(data, file, indent=4)
    file.truncate()  # remove remaining part


def main():
    global fixed_comment, mucks, mucks_Counter, yesterday_Mucks, consoleMode, preferences, thatWasCoolChains, muckCounts, totalComments
    if preferences["reduce comments"] == False:
        print(f"{color.RED}{color.BOLD}comment reduction is off{color.END}")

    # for every new comment:
    for comment in subreddit.stream.comments(skip_existing=True):
        totalComments += 1
        print(f"muck: {muckCounts}\nwow that was really cool: {thatWasCoolChains}\ntotal comments counted: {totalComments}")
        if consoleMode:
            break  # we shouldn't run the bot when using the console

        fixed_comment = fixComment(comment)

        # print comment details:
        printComment(comment.body, fixed_comment, comment.author.name)

        # skip the comment check if the commenter is the bot or the user is blocked:
        if comment.author.name == preferences["username"]:
            continue
        if comment.author.name.lower() in preferences["blocked users"]:
            print(f"{color.RED}USER BLOCKED{color.END}")
            continue

        # "wow that was really cool" chain detection:
        elif fuzz.ratio(fixed_comment,
                        "wothasrelyc") > 70:  # "wothasrelyc" is "wow that was really cool" after the comment processing
            if fuzz.ratio(fixComment(parent(comment)),
                          fixed_comment) > 80:  # only triggers if it's a part of a chain (parent comment needs to be similar)
                    thatWasCoolChains += 1

        # muck detection:
        else:
            for item in preferences["muck list"]:
                # if the comment is >74% "muck" and starts with "m"/"k":
                if fuzz.ratio(fixed_comment, item) > 74 and fixed_comment[0] in "mk":
                        print(f"{color.GREEN}MUCK detected! replying...{color.END}\n")
                        muckCounts += 1
            continue


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
        mainThread.start()

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