import unittest
import os
import requests

from utilities import HEADERS


class TestYoutubeApiKey(unittest.TestCase):
    def setUp(self):
        self.youtube_key = os.getenv("YOUTUBE_API")

    def test_youtube_api_key_is_defined(self):
        self.assertIsNotNone(self.youtube_key, msg="Missing YOUTUBE_API environment defined")

    def test_youtube_api_connection_status_code(self):
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q=YouTube+Data+API&type=video&key={self.youtube_key}'
        response = requests.get(url, HEADERS, timeout=5)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
