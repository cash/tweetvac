from tweetvac import TweetVac
import responses
import twython
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock


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
        body1 = b'[{"id": 200}, {"id": 100}]'
        url2 = self.createUrl(endpoint, {'max_id': '99'})
        body2 = b'[]'
        responses.add(responses.GET, url2, body=body2, match_querystring=True, content_type='application/json')
        responses.add(responses.GET, url1, body=body1, match_querystring=True, content_type='application/json')

        data = self.tweetvac.get(endpoint)

        self.assertEqual(2, len(data))

    @responses.activate
    def test_get_should_respect_max_requests(self):
        endpoint = 'statuses/user_timeline'
        url = self.createUrl(endpoint, {})
        body = b'[{"id": 200}, {"id": 100}]'
        responses.add(responses.GET, url, body=body, content_type='application/json')

        data = self.tweetvac.get(endpoint, max_requests=5)

        self.assertEqual(10, len(data))

    @responses.activate
    def test_get_with_filters(self):
        endpoint = 'statuses/user_timeline'
        url = self.createUrl(endpoint, {})
        body = b'[{"id": 200}, {"id": 100}, {"id": 50}, {"id": 25}, {"id": 10}, {"id": 5}]'
        responses.add(responses.GET, url, body=body, content_type='application/json')

        def f1(tweet):
            return tweet['id'] < 100

        def f2(tweet):
            return tweet['id'] > 10

        data = self.tweetvac.get(endpoint, filters=[f1, f2], max_requests=1)

        self.assertEquals(2, len(data))
        self.assertEquals(50, data[0]['id'])
        self.assertEquals(25, data[1]['id'])

    @responses.activate
    def test_get_with_cutoff(self):
        endpoint = 'statuses/user_timeline'
        url = self.createUrl(endpoint, {})
        body = b'[{"id": 200}, {"id": 100}]'
        responses.add(responses.GET, url, body=body, content_type='application/json')

        def f(tweet):
            return tweet['id'] == 100

        data = self.tweetvac.get(endpoint, cutoff=f)

        self.assertEquals(1, len(data))
        self.assertEquals(200, data[0]['id'])
