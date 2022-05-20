import configparser
config = configparser.ConfigParser()
config.read('./config.ini')

consumer_key = config.get('TwitterAPI','consumer_key')
consumer_secret = config.get('TwitterAPI','consumer_secret')
access_key = config.get('TwitterAPI','access_key')
access_secret = config.get('TwitterAPI','access_secret')


import tweepy
import json
import re       #url除去用
import datetime #ファイル名に使う現在日時
import schedule #定期実行用
from time import sleep

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#crawler
def main(keyword,count):
    data = dict()
    data['tweets'] = []
    filters = "-filter:retweets -filter:links -filter:replies -filter:images -filter:videos"
    tweets = api.search_tweets(q=keyword + filters, lang="ja",locale="ja", count=count,tweet_mode='extended' , geocode = "33.5654326,130.3386218,30km")
    for tweet in tweets:
        data["tweets"].append(
            {
                'keyword' : keyword,
                'name' : tweet.user.name,
                'id' : tweet.user.id,
                'follower' : tweet.user.followers_count,
                'friends' : tweet.user.friends_count,
                'user description' : tweet.user.description,
                'tweet id' : tweet.id,
                'text' : re.sub("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", "", tweet.full_text),
                'favorite count' : tweet.favorite_count,
                'retweet count' : tweet.retweet_count,
                },)
        try:
            api.create_favorite(tweet.id)
            api.create_friendship(user_id=tweet.user.id)
        except Exception as e:
            print(e)

    dt = datetime.datetime.now()
    dt_prt = str(dt.year) + '_' + str(dt.month) + '_' + str(dt.day) + '_' + str(dt.hour) + '_' + str(dt.minute) + '_' + str(dt.second)
    filename = 'Tweetsdata'+ dt_prt

    #print(json.dumps(data, ensure_ascii=False, indent=2))
    print("done")
    with open(filename+'.json', mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

main("",2)

#定期実行文
"""
if __name__ == "__main__":
    schedule.every(20).minutes.do(main,"",40)
    main("",40)
    while True:
        schedule.run_pending()
        sleep(1)
"""
