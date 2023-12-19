import logging
import unittest
from operator import itemgetter
import time
import ical_parser
import urllib.request
from icalendar import Calendar
from app import app

log = logging.getLogger(__name__)


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        # self.app.testing = True

    def test_smart(self):
        # maybe one day I can dynmically create this?
        test_list = [
            "2023-12-23 12:00:00-06:00",
            "2023-12-24 12:00:00-06:00",
            "2023-12-25 12:00:00-06:00",
            "2023-12-26 12:00:00-06:00",
            "2023-12-27 12:00:00-06:00",
            "2023-12-28 12:00:00-06:00",
            "2023-12-29 12:00:00-06:00",
            "2023-12-30 12:00:00-06:00",
            "2024-01-01 12:00:00-06:00",
            "2024-01-02 12:00:00-06:00",
            "2024-01-03 12:00:00-06:00",
            "2024-01-04 12:00:00-06:00",
            "2024-01-05 12:00:00-06:00",
            "2024-01-06 12:00:00-06:00",
            "2024-01-07 12:00:00-06:00",
            "2024-01-08 12:00:00-06:00",
            "2024-01-09 12:00:00-06:00",
        ]
        for test in test_list:
            results = ical_parser.smart_date(test)
            print("the results are: {}".format(results))
            print("------------------")
            self.assertIsNotNone(results)

    def test_self(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

    def test_app(self):
        url = "http://p27-calendars.icloud.com/published/2/sAKB2qXoM7Kj0E4v8n2nzd3naihwmKKZqvpklvflY9V-xB0-vg5pkFqB2dAyd_84"
        ics = urllib.request.urlopen(url).read()
        cal = Calendar.from_ical(ics)
        entries = []
        entries = ical_parser.ical_parser(cal)
        sorted_events = sorted(entries, key=itemgetter("date"))
        filtered = [
            i for i in sorted_events if i["date"] >= time.strftime("%Y-%m-%d %H:%M:%S")
        ]
        self.assertIsNotNone(ics)
        self.assertIsNotNone(cal)
        self.assertIsNotNone(filtered)

    def test_cal(self):
        result = self.app.get("/get_calendar")
        self.assertEqual(result.status_code, 200)

    def test_news(self):
        result = self.app.get("/get_news_headlines")
        self.assertEqual(result.status_code, 200)

    def test_weather(self):
        result = self.app.get("/get_weather")
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.data)

    def test_compliment(self):
        result = self.app.get("/get_compliment")
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.data)


if __name__ == "__main__":
    unittest.main()
