# tweet-favo-bot
TwitterAPI enable you to favo tweet and follow user automatically.  
you can specify keyword , the number of tweet(user) and geocode.  

## At first
you need Twitter development account.
make `config.ini`

```
[TwitterAPI]
consumer_key= your cousumer_key
consumer_secret = your consumer_secret
access_key= your access_key
access_secret = your access_secret
```

## User Settings
- keyword : search tweet that contain this keyword
- count : the number of tweet(user) you want to favo(follow)
- geocode : latitude , longitude , radius  
It runs regularly every 20 minutes.
