# this bot was made by u/hananelroe on reddit
import thefuzz.fuzz as fuzz
from thefuzz import *
import praw
print(praw.__version__)

Muck_list = ["muck", "muck.", "muck!", "muck?",
             "mück", "mück.", "mück!", "mück?",
             "m u c k", "m uck", "muc k", "mu ck",
             "muuck", "mu c k"]
# u/MaybeAnonymousDev added "m uck", "muc k", "mu ck", "muuck", and "mu c k"; note: no need to keep this comment here
IsMuck = False

# initialize with appropriate values
client_id = ""
client_secret = ""
username = "DaniDevChainBreaker"
password = ""
user_agent = "u/hananelroe's comment chains breaker bot"

# creating an authorized reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

subreddit = reddit.subreddit("DaniDev")
for comment in subreddit.stream.comments(skip_existing=True):
    print(comment.body)
    # check if the comment is above 74% muck: (allows 1 wrong letter in a 4 letters word)
    for item in Muck_list:
        if fuzz.ratio(comment.body.lower(), item) > 74:
            IsMuck = True
    if IsMuck:
        comment.reply("#**SHUT**\n___\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))")
        IsMuck = False
