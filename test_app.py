import unittest
from operator import itemgetter
import time
import ical_parser
import urllib.request
from icalendar import Calendar
from app import app


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_self(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_app(self):
        url = 'http://p27-calendars.icloud.com/published/2/sAKB2qXoM7Kj0E4v8n2nzd3naihwmKKZqvpklvflY9V-xB0-vg5pkFqB2dAyd_84'
        ics = urllib.request.urlopen(url).read()
        cal = Calendar.from_ical(ics)
        entries = []
        entries = ical_parser.ical_parser(cal)
        sorted_events = sorted(entries, key=itemgetter('date'))
        filtered = [i for i in sorted_events if i['date'] >= time.strftime(
            "%Y-%m-%d %H:%M:%S")]
        self.assertIsNotNone(filtered)

    def test_cal(self):
        result = self.app.get('/get_calendar')
        self.assertEqual(result.status_code, 200)

    def test_news(self):
        result = self.app.get('/get_news_headlines')
        self.assertEqual(result.status_code, 200)

    def test_compliment(self):
        result = self.app.get('/get_compliment')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.data)


if __name__ == '__main__':
    unittest.main()
