#!/usr/bin/python3
# this bot was made by u/hananelroe on reddit
import thefuzz.fuzz as fuzz
import praw
import unicodedata
import DA_SECRETS

print("\u001b[31;1m" + str(praw.__version__))

Muck_list = ["muck", "muck.", "muck!", "muck?", "mֳ¼ck", "mֳ¼ck.", "mֳ¼ck!", "mukc", "mֳ¼ck?", "m u c k", "m\\*ck",
             "kcum", "׀¼uck", "much", "mcuk", "mcak", "mack", "mucke", "mmuck", "mucka", "mucko", "mucki", "mucku",
             "muckk", "muckl", "muckm", "muckn", "mucko", "muckp", "muckq", "muckr", "mucks", "muckt", "mucku",
             "muckv", "muckw", "muckx", "mucky", "muckz", "muck0", "muck1", "muck2", "muck3", "muck4", "muck5",
             "muck6", "muck7", "muck8", "muck9", "muck!", "muck?", "muck.", "muck,", "muck;", "muck:", "muck-",
             "muck_", "muck+", "muck=", "muck/", "muck*", "muck@", "muck#", "muck$", "muck%", "muck^", "muck&",
             "muck(", "muck)", "muck[", "muck]", "muck{", "muck}", "muck|", "muck~", "muck`", "muck\"", "muck'",
             "muck<", "muck>", "muck\\", "muck\n", "muck\t", "muck\r", "muck\f", "muck\v", "muck\b", "muck\a",
             "muck\\e", "muck\x00", "muck\x01", "muck\x02", "muck\x03", "muck\x04", "muck\x05", "muck\x06",
             "muck\x07", "muck\x08", "muck\x09", "muck\x0a", "muck\x0b", "muck\x0c", "muck\x0d", "muck\x0e",
             "muck\x0f", "muck\x10", "muck\x11", "muck\x12", "muck\x13", "muck\x14", "muck\x15", "muck\x16",
             "muck\x17", "muck\x18", "muck\x19", "muck\x1a", "muck\x1b", "muck\x1c", "muck\x1d", "muck\x1e",
             "muck\x1f", "muck\x7f", "muck\x80", "muck\x81", "muck\x82", "muck\x83", "muck\x84", "muck\x85",
             "muck\x86", "muck\x87", "muck\x88", "muck\x89", "muck\x8a", "muck\x8b", "muck\x8c", "muck\x8d",
             "muck\x8e", "muck\x8f", "muck\x90", "muck\x91", "muck\x92", "muck\x93", "muck\x94", "muck\x95",
             "muck\x96", "muck\x97", "muck\x98", "muck\x99", "muck\x9a", "muck\x9b", "muck\x9c", "muck\x9d",
             "muck\x9e", "muck\x9f", "muck\xa0", "muck\xa1", "muck\xa2", "muck\xa3", "muck\xa4", "muck\xa5",
             "muck\xa6", "muck\xa7", "muck\xa8", "muck\xa9", "muck\xaa", "muck\xab", "muck\xac", "muck\xad",
             "muck\xae", "muck\xaf", "muck\xb0", "muck\xb1", "muck\xb2", "muck\xb3", "muck\xb4", "muck\xb5",
             "muck\xb6", "muck\xb7", "muck\xb8", "muck\xb9", "muck\xba", "muck\xbb", "muck\xbc", "muck\xbd",
             "muck\xbe", "muck\xbf", "muck\xc0", "muck\xc1", "muck\xc2", "muck\xc3", "muck\xc4", "muck\xc5",
             "muck\xc6", "muck\xc7"]
Blocked_users = ["u/DaniDevChainBreaker", "Hananelroe"]
Enable_Blocking = False

# initialize with appropriate values
client_id = DA_SECRETS.client_id
client_secret = DA_SECRETS.client_secret
username = DA_SECRETS.username
password = DA_SECRETS.password
user_agent = "u/hananelroe's and u/norecap_bot's comment chains breaker bot"
comment_content = "#**SHUT**\n___\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))\n\n ^(oh and if you're a real boner - upvote this comment. it helps my karma.)\n\n^(also here is your IP: 127.0.0.1 LOL)\n\n^(I'm a collaboration between [u/\u200cHananelroe](https://www.reddit.com/u/Hananelore) and [u/\u200cnorecap_bot](https://www.reddit.com/u/norecap_bot))"
why = "WHY?\n\n^(I'm a collaboration between u/Hananelroe and u/norecap_bot! we are breaking muck, much, mukc and etc chains)\n\n^(if you're a real boner - upvote this comment. it helps my karma.)"
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
            if comment.author.name in Blocked_users and IsBlocked:
                continue
            fixed_comment = noglyph("".join(dict.fromkeys(comment.body.lower())))
            print("\u001b[35;1m" + comment.body + "\u001b[34;1m\t" + fixed_comment + " \u001b[0m" + str(
                fuzz.ratio(fixed_comment, "muck")) + "%")
            if comment.author.name in Blocked_users and Enable_Blocking:
                print("u/\u001b[31;1m" + str(comment.author) + "\u001b[92mBLOCKED\u001b[0m")
                continue
            else:
                print("u/\u001b[36;1m" + str(comment.author) + "\u001b[0m")

            if parent(comment).author.name == username and comment.body.lower() == "bad bot":
                comment.reply(why)
            else:
                for item in Muck_list:
                    if fuzz.ratio(fixed_comment, item) > 74:
                        print("\033[92mMATCH! replying...\u001b[0m\n")
                        comment.reply(comment_content)
                        break
            continue
    except KeyboardInterrupt:  # Ctrl-C - stop
        print("\u001b[31;1mBye!\u001b[0m")
        break
    except Exception as error:
        print(f'\x1b[31;1mError: {error}')
        print('Trying to restart...\x1b[0m')
