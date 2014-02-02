tweetvac
========

Python package for sucking down tweets from Twitter. It implements Twitter's
[guidelines for working with timelines](https://dev.twitter.com/docs/working-with-timelines)
so that you don't have to.

tweetvac supports retrospective pulling of tweets from Twitter. For example, it
can pull down a large number of tweets by a specific user or all the tweets
from a geographic area that mentions a search term. It automatically generates
the requests to work backward along the timeline.

Requirements
============
tweetvac requires [twython](https://github.com/ryanmcgrath/twython) which can be
installed using pip or easy_install.

Authentication
==============
Twitter requires OAuth. tweetvac can store a user's authentication information
in a configuration file for reuse.

  1. Log into Twitter and open [https://dev.twitter.com/apps](https://dev.twitter.com/apps).
  2. Create a new application. The name needs to be unique across all Twitter apps. A callback is not needed.
  3. Create an OAuth access token on your application web page.
  4. Create a file called tweetvac.cfg and format it as follows:

```
[Auth]
consumer_key = Gx33LSA3IICoqqPoJOp9Q
consumer_secret = 1qkKAljfpQMH9EqDZ8t50hK1HbahYXAUEi2p505umY0
oauth_token = 14574199-4iHhtyGRAeCvVzGpPNz0GLwfYC54ba3sK5uBl4hPe
oauth_token_secret = K80YytdT9FRXEoADlVzJ64HDQEaUMwb37N9NBykCNw5gw
```

Alternatively, you can pass those four parameters as a tuple in the above order
into the `Tweetvac` constructor rather than storing them in a configuration file.

The Basics
==========

Creating a Tweetvac instance
----------------------------
You can pass the OAuth parameters as a tuple:

```python
vac = tweetvac.TweetVac((consumer_key, consumer_secret, oauth_token, oauth_token_secret))
```

or use the configuration object:

```python
config = tweetvac.TweetVacAuthConfig()
vac = tweetvac.TweetVac(config)
```

Sucking down tweets
--------------------

tweetvac expects a Twitter endpoint and a dictionary of parameters for that
endpoint. Read the [Twitter documentation](https://dev.twitter.com/docs/api/1.1)
for a list of endpoints and their parameters. It is recommended to set the count
option in the params dict to the largest value supported by that endpoint.

```python
params = {'screen_name': 'struckDC', 'count': 200}
data = vac.get('statuses/user_timeline', params)
```

Saving data
------------
The data returned is a list of dicts and can be serialized into json for storage.

```python
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)
```

Advanced
=========

Filtering the tweets
--------------------
Twitter provides several parameters on each endpoint for selecting what tweets
you want to retrieve. Additional culling is available by passing a list of filter
functions.

```python
def remove_mention_tweets(tweet):
    return not '@' in tweet['text']

data = vac.get('statuses/user_timeline', params, filters=[remove_mention_tweets])
```

Return false from your function to remove the tweet from the list that will be
returned to you.

Turning off the vacuum
-----------------------
tweetvac will suck down tweets until you reach your rate limit or you consume all
the available tweets. To stop sooner, you can pass a cutoff function that returns
true when tweetvac should stop.

```python
def stop(tweet):
    cutoff_date = time.strptime("Wed Jan 01 00:00:00 +0000 2014", '%a %b %d %H:%M:%S +0000 %Y')
    tweet_date = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    return tweet_date < cutoff_date

data = vac.get('statuses/user_timeline', params, cutoff=stop)
```

You can also pass a hard limit to the number of requests to stop tweetvac early:

```python

data = vac.get('statuses/user_timeline', params, max_requests=10)
```

Twitter API
===========
Supported Endpoints
--------------------
 * [statuses/user_timeline](https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline) - tweets by the specified user.
 * [statuses/home_timeline](https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline) - tweets by those followed by the authenticating user.
 * [statuses/mentions_timeline](https://dev.twitter.com/docs/api/1.1/get/statuses/mentions_timeline) - tweets mentioning the authenticating user.
 * [statuses/retweets_of_me](https://dev.twitter.com/docs/api/1.1/get/statuses/retweets_of_me) - tweets that are retweets of the authenticating user.
 * [search/tweets](https://dev.twitter.com/docs/api/1.1/get/search/tweets) - search over tweets

 The endpoints have different request rate limits, count limits per request, and total tweet count limits.
