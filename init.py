from time import sleep
import tweepy
import praw

from config import config
from keys import keys

copyFrom = config['twitter_user']
postTo = config['reddit_sub']
mentionRT = config['mention_rt']
mentionMI = config['mention_mi']
mentionIm = config['mention_im']

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
        if hasattr(newTweet, 'retweeted_status'):
            newTweet = newTweet.retweeted_status
            reTweet = True
        else:
            reTweet = False

        fullTweetText = newTweet.full_text

        mediaUrl = []
        if 'media' in newTweet.entities:
            for media in newTweet.extended_entities['media']:
                mediaUrl.append(media['media_url'])

        try:
            flair = ""
            if len(mediaUrl) == 1:  # Just one media
                post = reddit.subreddit(postTo).submit(title=fullTweetText, url=mediaUrl)
                flair += mentionIm + " | "

            elif len(mediaUrl) > 1:  # More than one media file
                postText = ""
                for item in mediaUrl:
                    postText += item + "\n\n"
                post = reddit.subreddit(postTo).submit(title=fullTweetText + mentionMI, selftext=postText)
                flair += mentionMI + " | "

            else:  # No media just the title
                post = reddit.subreddit(postTo).submit(title=fullTweetText, selftext="")

            if reTweet:
                flair += mentionRT

            if len(flair) != 0:
                sleep(5)
                if str(post.link_flair_text) != "None":
                    post.mod.flair(str(post.link_flair_text) + " | " + str(flair))
                else:
                    post.mod.flair(str(flair))

        except Exception as e:
            print("Error, please copy this and open a issue on the git page with this info:")
            print("Error Code: " + str(e))

        print("Tweet: /t" + fullTweetText)
        lastTweet = newTweet.id
    sleep(11 * 60)
