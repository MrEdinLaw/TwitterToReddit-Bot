import tweepy
import requests

auth = tweepy.OAuth1UserHandler(
   "OUqSjaptCgthC4EBslVxsMgQC", "bb9wIiuE7SRU3JVfAJ1UUouKl4OoT5tthIFGoObXP8BZwkyVZJ", "1549518097119322113-ynR6rPCiHBtDQNqgsGC3wJBST82nUC", "gImLBJ6JlWOMojDat8ZOH8AWeB3hyMHMw9NY4qvzMSSbE"
)

API = tweepy.API(auth)

acc1 = "1500tasvir_en"
accT = "AlexanderShad4"

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('M6zCxP0NGuiuRcPqGBq2-g', 'W6BPhsbDTCTqlunPQSSUEUZf31ueKw')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'EyIranTwitter-Bot',
        'password': 'dapice6765'}

    # setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'EyIranTwitter-Bot/0.0.1'}

    # send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

print('New OAuth Redeemed')
latestTweet1 = API.user_timeline(screen_name=accT,count=1)[0].text

while True:
    for tweet1 in API.user_timeline(screen_name=accT,count=1):
        if latestTweet1 != tweet1.text:
            print("New Tweet: " + tweet1.text)
            latestTweet1 = tweet1.text

            requests.post("https://oauth.reddit.com/api/submit", params={"title": tweet1.text, "sr": "r/doggomoggo"}, headers=headers)

            # print(requests.get('https://oauth.reddit.com/api/v1/me', headers=headers))
