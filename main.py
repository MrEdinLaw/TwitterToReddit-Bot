import tweepy
import praw

from keysnshit import twitterKeys, redditKeys

auth = tweepy.OAuth1UserHandler(
   twitterKeys["ConsumerKey"], twitterKeys["ConsumerKeySecret"], twitterKeys["AccessKey"], twitterKeys["AccessKeySecret"]
)

API = tweepy.API(auth)

reddit = praw.Reddit(
    client_id=redditKeys["PUS"],
    client_secret=redditKeys["Secret"],
    password=redditKeys["Password"],
    username=redditKeys["Username"]
)

# print(reddit.user.me())

acc1 = "AlexanderShad4" # Example Twitter Account

latestTweet1 = API.user_timeline(screen_name=acc1, count=1)[0].text

def eventSource1(latestTweet1):
    if latestTweet1 != API.user_timeline(screen_name=acc1, count=1)[0].text:

        # Trigger Reddit Post
        print("New Tweet: " + API.user_timeline(screen_name=acc1, count=1)[0].text)

        # Reset Loop
        latestTweet1 = API.user_timeline(screen_name=acc1, count=1)[0].text

    return latestTweet1

# Event Loop
while True:
    latestTweet1 = eventSource1(latestTweet1)
