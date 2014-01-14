from __future__ import unicode_literals

import twython
import ConfigParser


# TODO: catch common problems and display friendly error messages


class TwitterAuthConfig(object):
    """Twitter authorization tool"""

    def __init__(self, filename='tweetvac.cfg'):
        self._config = ConfigParser.RawConfigParser()
        self._config_filename = filename
        self.consumer_key = ''
        self.consumer_secret = ''
        self.oauth_token = ''
        self.oauth_token_secret = ''

    def load(self):
        """Load the authorization information from the config file"""

        self._config.read(self._config_filename)
        try:
            self.consumer_key = self._config.get('Auth', 'consumer_key')
            self.consumer_secret = self._config.get('Auth', 'consumer_secret')
            self.oauth_token = self._config.get('Auth', 'oauth_token')
            self.oauth_token_secret = self._config.get('Auth', 'oauth_token_secret')
        except ConfigParser.NoSectionError:
            raise TwitterAuthException("No data")

    def set(self, auth_params):
        """Set the authorization information

        :param auth_params: consumer_key, consumer_secret, oauth_token, oauth_secret as tuple.
        """

        (self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_token_secret) = auth_params

    def save(self):
        """Save the authorization information to the config file"""

        self._config.add_section('Auth')
        self._config.set('Auth', 'consumer_key', self.consumer_key)
        self._config.set('Auth', 'consumer_secret', self.consumer_secret)
        self._config.set('Auth', 'oauth_token', self.oauth_token)
        self._config.set('Auth', 'oauth_token_secret', self.oauth_token_secret)

        with open(self._config_filename, 'wb') as config_file:
            self._config.write(config_file)


class TwitterAuthHelper(object):
    """"Helps a user through the OAuth process to get OAuth token"""

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
            print "Error: Invalid consumer key or consumer secret"

        pin = self._get_pin(auth_url)

        (oauth_token, oauth_secret) = self._get_oauth_token(request_token, request_secret, pin)

        return self.consumer_key, self.consumer_secret, oauth_token, oauth_secret

    def _get_consumer_data(self):
        """Return the user's app information (consumer token and secret)"""

        print "\nRegister this application with Twitter at https://dev.twitter.com/apps"
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

        print "\nApprove access to your data at " + request_auth_url
        return raw_input("Then enter the authorization PIN: ").strip()

    def _get_oauth_token(self,  request_token, request_token_secret, auth_pin):
        """Return the authorized oauth token and secret retrieved from Twitter"""

        twitter = twython.Twython(self.consumer_key, self.consumer_secret, request_token, request_token_secret)
        oauth = twitter.get_authorized_tokens(auth_pin)
        return oauth['oauth_token'], oauth['oauth_token_secret']


class TwitterAuthException(Exception):
    """An error with authorization occurred."""

