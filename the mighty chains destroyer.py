#!/data/data/com.termux/files/usr/bin/python3
# this bot was made by u/hananelroe on reddit
import thefuzz.fuzz as fuzz
from thefuzz import *
import praw
import unicodedata


def noglyph(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


print(praw.__version__)

# Muck_list = ["#**SHUT**\n___\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))\n\n ^(oh and if you're a real boner - upvote this comment. it helps my karma.)"]
Muck_list = ["muck", "muck.", "muck!", "muck?", "mֳ¼ck", "mֳ¼ck.", "mֳ¼ck!", "mukc", "mֳ¼ck?", "m u c k", "m\*ck",
             "kcum", "׀¼uck", "mick", "much", "mcuk"]
Blocked_users = []

# initialize with appropriate values
client_id = ""
client_secret = ""
username = ""
password = ""
user_agent = "u/hananelroe's and u/norecap_bot's comment chains breaker bot"
comment_content = "#**SHUT**\n___\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))\n\n ^(oh and if you're a real boner - upvote this comment. it helps my karma.)\n^(also here is your IP: 127.0.0.1 LOL)\n^(I'm a collaboration between u/DaniDevChainBreaker and u/norecap_bot)"
why = "WHY?\n\n^(this is a port of the dani dev chain breaker! we are breaking muck, much, mukc and etc chains)\n\n^(if you're a real boner - upvote this comment. it helps my karma.)"
com = ""

while True:
    # creating an authorized reddit instance
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    subreddit = reddit.subreddit("DaniDev")
    print("online")

    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            com = noglyph("".join(dict.fromkeys(comment.body.lower())))
            print("\u001b[35;1m" + comment.body + "\u001b[34;1m\t" + com + " \u001b[0m" + str(fuzz.ratio(com, "muck")))
            print("\u001b[36;1m" + str(comment.author) + "\u001b[0m")

            if comment.parent().author.name == username and comment.body.lower() == "bad bot":
                comment.reply(why)
                break
            else:
                for item in Muck_list:
                    if fuzz.ratio(com, item) > 74:
                        for user in Blocked_users:
                            if str(comment.author) == user:
                                comment.reply(comment_content)
                                break
    except KeyboardInterrupt:  # Ctrl-C - stop
        print("Bye!")
        break
    except Exception as error:  # Any exception
        print(f"Error: {error}")
        print("Trying to restart...")
