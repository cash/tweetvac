from tweetvac import TweetVac
import responses
import twython
import urllib
try:
    import unittest.mock as mock
except ImportError:
    import mock
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    import unittest2 as unittest
else:
    import unittest


class TweetVacTestCase(unittest.TestCase):

    def setUp(self):
        self.tweetvac = TweetVac(('', '', '', ''))

    def createUrl(self, endpoint, params):
        url = 'https://api.twitter.com/1.1/' + endpoint + '.json'
        if params:
            url += '?' + urllib.urlencode(params)
        return url

    def test_get_should_handle_rate_limit_error(self):
        with mock.patch.object(twython.Twython, 'get') as get_mock:
            get_mock.side_effect = twython.TwythonRateLimitError('', 429, False)

            data = self.tweetvac.get('')

            self.assertEqual([], data)
            self.assertTrue(self.tweetvac.hit_rate_limit)

    @responses.activate
    def test_get_should_stop_when_no_data(self):
        endpoint = 'statuses/user_timeline'
        url1 = self.createUrl(endpoint, {})
        body1 = '[{"id": 200}, {"id": 100}]'
        url2 = self.createUrl(endpoint, {'max_id': '99'})
        body2 = '[]'
        responses.add(responses.GET, url2, body=body2, match_querystring=True, content_type='application/json')
        responses.add(responses.GET, url1, body=body1, match_querystring=True, content_type='application/json')

        data = self.tweetvac.get(endpoint)

        self.assertEqual(2, len(data))

    @responses.activate
    def test_get_should_respect_max_requests(self):
        endpoint = 'statuses/user_timeline'
        url = self.createUrl(endpoint, {})
        body = '[{"id": 200}, {"id": 100}]'
        responses.add(responses.GET, url, body=body, content_type='application/json')

        data = self.tweetvac.get(endpoint, max_requests=5)

        self.assertEqual(10, len(data))
