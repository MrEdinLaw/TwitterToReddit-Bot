from time import sleep
import tweepy
import praw

from config import config
from keys import keys

copyFrom = config['twitter_user']
postTo = config['reddit_sub']

# REST API connection
reddit = praw.Reddit(client_id=keys['reddit_client_id'],
                     client_secret=keys['reddit_client_secret'],
                     user_agent=keys['reddit_user_agent'],
                     username=config['reddit_username'],
                     password=config['reddit_password'])

# Twitter Api Connection
auth = tweepy.OAuthHandler(keys['twitter_consumer_key'], keys['twitter_consumer_secret'])
auth.set_access_token(keys['twitter_access_token'], keys['twitter_access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_last_tweet(self):
    tweet = self.user_timeline(copyFrom, count=1, tweet_mode="extended", include_entities=True)[0]
    return tweet


lastTweet = 0
while True:
    newTweet = get_last_tweet(api)
    if newTweet.id != lastTweet:

        mediaUrl = 0
        if 'media' in newTweet.entities:
            for media in newTweet.entities['media']:
                mediaUrl = media['media_url']

        if mediaUrl != 0:
            reddit.subreddit(postTo).submit(title=newTweet.full_text, url=mediaUrl)
        else:
            reddit.subreddit(postTo).submit(title=newTweet.full_text, selftext="")

        print(newTweet.full_text)
        lastTweet = newTweet.id
    sleep(11 * 60)
