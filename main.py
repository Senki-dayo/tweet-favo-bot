import configparser
from itertools import count
import tweepy
import json
import re
import datetime
import schedule
from time import sleep

# User Setting
keyword = ""
count = 2
geocode = "33.5654326,130.3386218,30km"

# read config
config = configparser.ConfigParser()
config.read('./config.ini')

# read key
consumer_key = config.get('TwitterAPI','consumer_key')
consumer_secret = config.get('TwitterAPI','consumer_secret')
access_key = config.get('TwitterAPI','access_key')
access_secret = config.get('TwitterAPI','access_secret')

# set key
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#crawler
def main():
    data = dict()
    data['tweets'] = []
    filters = "-filter:retweets -filter:links -filter:replies -filter:images -filter:videos"
    tweets = api.search_tweets(q=keyword + filters, lang="ja",locale="ja", count=count,tweet_mode='extended' , geocode = geocode)
    for tweet in tweets:
        try:
            # fetch information
            data["tweets"].append(
                {
                    'keyword' : keyword,
                    'name' : tweet.user.name,
                    'id' : tweet.user.id,
                    'user description' : tweet.user.description,
                    'tweet id' : tweet.id,
                    'text' : re.sub("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", tweet.full_text),
                },)
            # favorite tweet
            api.create_favorite(tweet.id)
            # follow user
            api.create_friendship(user_id=tweet.user.id)
        except Exception as e:
            print(e)

    # make filename
    dt = datetime.datetime.now()
    dt_prt = str(dt.year) + '_' + str(dt.month) + '_' + str(dt.day) + '_' + str(dt.hour) + '_' + str(dt.minute) + '_' + str(dt.second)
    filename = 'Tweetsdata'+ dt_prt

    # dump jsonfile
    with open(filename+'.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print("done")


if __name__ == "__main__":
    schedule.every(20).minutes.do(main)
    main()
    while True:
        schedule.run_pending()
        sleep(1)
