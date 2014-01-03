from twython import Twython
import ConfigParser

# TODO: turn this into an authorization class
# TODO: catch common problems and display friendly error messages

config = ConfigParser.RawConfigParser()
config.read('tweetvac.cfg')
try:
    consumer_key = config.get('Auth', 'consumer_key')
    consumer_secret = config.get('Auth', 'consumer_secret')
    oauth_token = config.get('Auth', 'oauth_token')
    oauth_token_secret = config.get('Auth', 'oauth_token_secret')
    print oauth_token_secret
    exit()
except ConfigParser.NoSectionError:
    print "no data"


print "Register your application with Twitter at https://dev.twitter.com/apps"
consumer_key = raw_input("Enter your consumer key: ").strip()
consumer_secret = raw_input("Enter your consumer secret: ").strip()

twitter = Twython(consumer_key, consumer_secret)
auth = twitter.get_authentication_tokens()

request_oauth_token_secret = auth['oauth_token_secret']
request_oauth_token = auth['oauth_token']
request_auth_url = auth['auth_url']

print "\nApprove access to your data at " + request_auth_url
auth_pin = raw_input("Then enter the authorization PIN: ").strip()

twitter = Twython(consumer_key, consumer_secret, request_oauth_token, request_oauth_token_secret)

oauth = twitter.get_authorized_tokens(auth_pin)
oauth_token = oauth['oauth_token']
oauth_token_secret = oauth['oauth_token_secret']

config.add_section('Auth')
config.set('Auth', 'consumer_key', consumer_key)
config.set('Auth', 'consumer_secret', consumer_secret)
config.set('Auth', 'oauth_token', oauth_token)
config.set('Auth', 'oauth_token_secret', oauth_token_secret);

with open('tweetvac.cfg', 'wb') as config_file:
    config.write(config_file)






