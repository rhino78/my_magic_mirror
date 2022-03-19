import unittest
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
