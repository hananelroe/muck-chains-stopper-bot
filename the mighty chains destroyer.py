#!/usr/bin/python3
# this bot was made by u/hananelroe on reddit
# import needed libraries
import thefuzz.fuzz as fuzz
import praw
import unicodedata
import DA_SECRETS

# print the version
print("\u001b[31;1m" + str(praw.__version__))

Muck_list = ["muck", "muck.", "muck!", "muck?", "mֳ¼ck", "mֳ¼ck.", "mֳ¼ck!", "mukc", "mֳ¼ck?", "m\*ck",
             "kcum", "׀¼uck", "much", "mcuk"]
Blocked_users = [] # to use you need to write the user name without the "u/"
Enable_Blocking = False

# initialize with appropriate values
client_id = DA_SECRETS.client_id
client_secret = DA_SECRETS.client_secret
username = DA_SECRETS.username
password = DA_SECRETS.password
user_agent = "u/hananelroe's and u/HoseanRC's comment chains breaker bot"
comment_content = "#**SHUT**"
content = "\n___\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))\n\n ^(I'm a collaboration between [Hananelroe](https://www.reddit.com/u/Hananelroe) and [HoseanRC](https://www.reddit.com/u/HoseanRC))"
why = "WHY?" + content
thanks = "thanks! :)" + content
fixed_comment = ""


class Empty:
    pass


def parent(child_comment):
    parent_comment = Empty()
    parent_comment.author = ""
    try:
        parent_comment = child_comment.parent()
    finally:
        return parent_comment


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

    subreddit = reddit.subreddit("DaniDev")
    print("\033[92monline\u001b[0m")

    try:
        for comment in subreddit.stream.comments(skip_existing=True):
            fixed_comment = noglyph("".join(dict.fromkeys(comment.body.lower()))).replace(" ","").replace("\n","")
            print("\u001b[35;1m" + comment.body + "\u001b[34;1m\t" + fixed_comment + " \u001b[0m" + str(
                fuzz.ratio(fixed_comment, "muck")) + "%")
            if comment.author.name in Blocked_users and Enable_Blocking:
                print("u/\u001b[31;1m" + str(comment.author) + "\u001b[92mBLOCKED\u001b[0m")
                continue
            else:
                print("u/\u001b[36;1m" + str(comment.author) + "\u001b[0m")
                if comment.author.name == username:
                    continue
            if parent(comment).author.name == username and comment.body.lower() == "bad bot":
                print("\033[92mbad bot MATCH! replying...\u001b[0m\n")
                try:
                    comment.parent().parent().parent()
                except:
                    comment.reply(why)
                else:
                    comment.reply("WHY?")
                continue
            elif parent(comment).author.name == username and comment.body.lower() == "good bot":
                print("\033[92mgood bot MATCH! replying...\u001b[0m\n")
                try:
                    comment.parent().parent().parent()
                except:
                    comment.reply(thanks)
                else:
                    comment.reply("thanks :)")
                continue
            else:
                for item in Muck_list:
                    if fuzz.ratio(fixed_comment, item) > 74:
                        print("\033[92mMATCH! replying...\u001b[0m\n")
                        try:
                            comment.parent().parent().parent()
                        except:
                            comment.reply(comment_content + content)
                        else:
                            comment.reply(comment_content)
                        break
                continue
    except KeyboardInterrupt:  # Ctrl-C - stop
        print("\u001b[31;1mBye!\u001b[0m")
        break
    except Exception as error:  # Any exception
        print(f"\u001b[31;1mError: {error}")
        print("Trying to restart...\u001b[0m")
