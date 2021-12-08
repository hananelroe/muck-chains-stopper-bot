# this bot was made by u/hananelroe on reddit
import praw
print(praw.__version__)

Muck_list = ["muck", "muck.", "muck!", "muck?",
             "mück", "mück.", "mück!", "mück?"]

# initialize with appropriate values
client_id = ""
client_secret = ""
username = "hananelroe"
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
    if comment.body.lower() in Muck_list:
        comment.reply("###SHUT\n ^(I'm just a simple bot that wants to stop muck chains, [here is my source code](https://github.com/hananelroe/muck-chains-stopper-bot))")
