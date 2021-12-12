#!/usr/bin/python3
# this bot was made by u/hananelroe on reddit
# exception handeling and neating the code: u/n1k0nP on reddit
import thefuzz.fuzz as fuzz
import praw
import unicodedata

print("\u001b[31;1m" + str(praw.__version__))

Muck_list = ["muck", "muck.", "muck!", "muck?", "mֳ¼ck", "mֳ¼ck.", "mֳ¼ck!", "mukc", "mֳ¼ck?", "m u c k", "m\*ck",
             "kcum", "׀¼uck", "mick", "much", "mcuk"]
Blocked_users = ["u/DaniDevChainBreaker"]

# initialize with appropriate values
client_id = ""
client_secret = ""
username = "DaniDevChainBreaker"
password = ""
user_agent = "u/hananelroe's and u/norecap_bot's comment chains breaker bot"
comment_content = "#**SHUT**\n___\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))\n\n ^(oh and if you're a real boner - upvote this comment. it helps my karma.)\n^(also here is your IP: 127.0.0.1 LOL)\n^(I'm a collaboration between u/DaniDevChainBreaker and u/norecap_bot)"
why = "WHY?\n\n^(this is a port of the dani dev chain breaker! we are breaking muck, much, mukc and etc chains)\n\n^(if you're a real boner - upvote this comment. it helps my karma.)"
fixed_comment = ""

class Empty:
    pass

def parent(child_comment):
    parent_comment = Empty()
    parent_comment.author = ""
    try:
        parent_comment = child_comment.parent()
    finally:
        return (parent_comment)

def noglyph(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

while True:
    # creating an authorized reddit instance
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    subreddit = reddit.subreddit("test")
    print("\033[92monline\u001b[0m")

    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            fixed_comment = noglyph("".join(dict.fromkeys(comment.body.lower())))
            print("\u001b[35;1m" + comment.body + "\u001b[34;1m\t" + fixed_comment + " \u001b[0m" + str(fuzz.ratio(fixed_comment, "muck")) + "%")
            print("u/\u001b[36;1m" + str(comment.author) + "\u001b[0m\n")

            if parent(comment).author.name == username and comment.body.lower() == "bad bot":
                comment.reply(why)
                break
            else:
                for item in Muck_list:
                    if fuzz.ratio(fixed_comment, item) > 80:
                        for user in Blocked_users:
                            if str(comment.author) not in user:
                                print("\033[92mMATCH! replying...\u001b[0m")
                                comment.reply(comment_content)
                                break
    except KeyboardInterrupt:  # Ctrl-C - stop
        print("\u001b[31;1mBye!\u001b[0m")
        break
    except Exception as error:  # Any exception
        print(f"\u001b[31;1mError: {error}")
        print("Trying to restart...\u001b[0m")
