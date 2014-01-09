import twython
import ConfigParser

# TODO: catch common problems and display friendly error messages


class TwitterAuthConfig:
    config_filename = 'tweetvac.cfg'

    def __init__(self):
        self._config = ConfigParser.RawConfigParser()
        self.consumer_key = ''
        self.consumer_secret = ''
        self.oauth_token = ''
        self.oauth_token_secret = ''

    def load(self):
        if not self._get_config_from_file():
            self._get_config_from_user()
            self._save_config()

    def _get_config_from_file(self):
        self._config.read(TwitterAuthConfig.config_filename)
        try:
            self.consumer_key = self._config.get('Auth', 'consumer_key')
            self.consumer_secret = self._config.get('Auth', 'consumer_secret')
            self.oauth_token = self._config.get('Auth', 'oauth_token')
            self.oauth_token_secret = self._config.get('Auth', 'oauth_token_secret')
            success = True
        except ConfigParser.NoSectionError:
            success = False

        return success

    def _get_config_from_user(self):
        print "\ntweetvac is not configured. Launching the configuration helper..."
        print "\nRegister this application with Twitter at https://dev.twitter.com/apps"
        self.consumer_key = raw_input("Enter your consumer key: ").strip()
        self.consumer_secret = raw_input("Enter your consumer secret: ").strip()

        twitter = twython.Twython(self.consumer_key, self.consumer_secret)
        try:
            auth = twitter.get_authentication_tokens()
            request_oauth_token_secret = auth['oauth_token_secret']
            request_oauth_token = auth['oauth_token']
            request_auth_url = auth['auth_url']
        except twython.exceptions.TwythonAuthError:
            print "Error: Invalid comsumer key or consumer secret"

        print "\nApprove access to your data at " + request_auth_url
        auth_pin = raw_input("Then enter the authorization PIN: ").strip()
        twitter = twython.Twython(self.consumer_key, self.consumer_secret, request_oauth_token, request_oauth_token_secret)
        oauth = twitter.get_authorized_tokens(auth_pin)

        self.oauth_token = oauth['oauth_token']
        self.oauth_token_secret = oauth['oauth_token_secret']

    def _save_config(self):
        self._config.add_section('Auth')
        self._config.set('Auth', 'consumer_key', self.consumer_key)
        self._config.set('Auth', 'consumer_secret', self.consumer_secret)
        self._config.set('Auth', 'oauth_token', self.oauth_token)
        self._config.set('Auth', 'oauth_token_secret', self.oauth_token_secret)

        with open(TwitterAuthConfig.config_filename, 'wb') as config_file:
            self._config.write(config_file)


config = TwitterAuthConfig()
config.load()
print config.consumer_key
