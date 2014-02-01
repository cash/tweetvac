from __future__ import unicode_literals

import twython
import ConfigParser


class TweetVac(object):
    """Suck down tweets using Twitter's API"""

    def __init__(self, config):
        """Construct a TweetVac object

        :param config: A tuple of auth parameters or a TweetVacAuthConfig object. The tuple
                       should be ordered as (consumer_key, consumer_secret, oauth_token, oauth_secret)
        """

        self.hit_rate_limit = False
        if isinstance(config, TweetVacAuthConfig):
            if not config.is_loaded():
                config.load()
            self.config = config.get()
        else:
            self.config = config

    def get(self, endpoint, params=None, cutoff=None, filters=None, max_requests=15):
        """Get a list of tweets

        :param endpoint: The twitter endpoint to call (ex. 'statuses/user_timeline')
        :param params: Parameters as dict for twitter endpoint
        :param cutoff: Optional function that returns true to stop the process
        :param filters: Optional function that removes tweets from each batch
        :param max_requests: Optional number of requests to make before stopping
        """

        twitter = twython.Twython(*self.config)

        data = []
        request_counter = 0
        self.hit_rate_limit = False
        while True:
            try:
                batch = twitter.get(endpoint, params)
            except twython.exceptions.TwythonRateLimitError:
                self.hit_rate_limit = True
                return data

            request_counter += 1

            if not batch:
                break

            if filters is not None:
                for f in filters:
                    batch = filter(f, batch)

            if cutoff is not None and cutoff(batch[-1]):
                batch = [item for item in batch if not cutoff(item)]
                # set stopping condition
                max_requests = request_counter

            data.extend(batch)
            params['max_id'] = batch[-1]['id'] - 1

            if request_counter == max_requests:
                break

        return data


class TweetVacAuthConfig(object):
    """Twitter authorization configuration tool"""

    def __init__(self, filename='tweetvac.cfg'):
        """Construct a TweetVacAuthConfig object

        :param filename: Optional filename of the configuration (default is tweetvac.cfg)
        """

        self._config = ConfigParser.RawConfigParser()
        self._config_filename = filename
        self.consumer_key = None
        self.consumer_secret = None
        self.oauth_token = None
        self.oauth_token_secret = None

    def is_loaded(self):
        """Is the authorization information loaded or set"""

        return self.consumer_key is not None and self.consumer_secret is not None and \
            self.oauth_token is not None and self.oauth_token_secret is not None

    def load(self):
        """Load the authorization information from the config file"""

        self._config.read(self._config_filename)
        try:
            self.consumer_key = self._config.get('Auth', 'consumer_key')
            self.consumer_secret = self._config.get('Auth', 'consumer_secret')
            self.oauth_token = self._config.get('Auth', 'oauth_token')
            self.oauth_token_secret = self._config.get('Auth', 'oauth_token_secret')
        except ConfigParser.NoSectionError:
            raise TweetVacAuthException("No data")

    def set(self, auth_params):
        """Set the authorization information

        :param auth_params: consumer_key, consumer_secret, oauth_token, oauth_secret as tuple.
        """

        (self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_token_secret) = auth_params

    def get(self):
        """Get the authorization information as tuple"""

        return self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_token_secret

    def save(self):
        """Save the authorization information to the config file"""

        self._config.add_section('Auth')
        self._config.set('Auth', 'consumer_key', self.consumer_key)
        self._config.set('Auth', 'consumer_secret', self.consumer_secret)
        self._config.set('Auth', 'oauth_token', self.oauth_token)
        self._config.set('Auth', 'oauth_token_secret', self.oauth_token_secret)

        with open(self._config_filename, 'wb') as config_file:
            self._config.write(config_file)


class TweetVacAuthHelper(object):
    """"Interactive helper for getting an OAuth token"""

    def __init__(self, consumer_key=None, consumer_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def run(self):
        """Run the helper and return the oauth tokens"""

        if not self.consumer_key and not self.consumer_secret:
            (self.consumer_key, self.consumer_secret) = self._get_consumer_data()

        try:
            (request_token, request_secret, auth_url) = self._get_request_token()
        except twython.exceptions.TwythonAuthError:
            print("Error: Invalid consumer key or consumer secret")

        pin = self._get_pin(auth_url)

        (oauth_token, oauth_secret) = self._get_oauth_token(request_token, request_secret, pin)

        return self.consumer_key, self.consumer_secret, oauth_token, oauth_secret

    def _get_consumer_data(self):
        """Return the user's app information (consumer token and secret)"""

        print("\nRegister this application with Twitter at https://dev.twitter.com/apps")
        consumer_key = raw_input("Enter your consumer key: ").strip()
        consumer_secret = raw_input("Enter your consumer secret: ").strip()
        return consumer_key, consumer_secret

    def _get_request_token(self):
        """Return the request token retrieved from Twitter"""

        twitter = twython.Twython(self.consumer_key, self.consumer_secret)
        auth = twitter.get_authentication_tokens()
        return auth['oauth_token'], auth['oauth_token_secret'], auth['auth_url']

    def _get_pin(self, request_auth_url):
        """Return authorization pin from user"""

        print("\nApprove access to your data at " + request_auth_url)
        return raw_input("Then enter the authorization PIN: ").strip()

    def _get_oauth_token(self,  request_token, request_token_secret, auth_pin):
        """Return the authorized oauth token and secret retrieved from Twitter"""

        twitter = twython.Twython(self.consumer_key, self.consumer_secret, request_token, request_token_secret)
        oauth = twitter.get_authorized_tokens(auth_pin)
        return oauth['oauth_token'], oauth['oauth_token_secret']


class TweetVacAuthException(Exception):
    """An error with authorization occurred."""
