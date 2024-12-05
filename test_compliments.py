"""a test suite for all tests in compliments"""

import unittest
import compliments
import api_interface


class TestCompliments(unittest.TestCase):
    """a test class to test all compliments"""

    def testlist(self):
        """test the list function"""
        listresult = api_interface.getquotes()
        self.assertIsNotNone(listresult)

    def testcompliment(self):
        """test the overall compliments"""
        compliments.compliment()
        complimentresult = compliments.compliment()
        self.assertIsNotNone(complimentresult)

    def testsummer(self):
        """test the summer compliment"""
        summer = api_interface.getsummer()
        print(summer)
        self.assertIsNotNone(summer)

    def testtips(self):
        """tests that we got a good tip"""
        tips = api_interface.gettips()
        print(tips)
        self.assertIsNotNone(tips)

    def testholiday(self):
        """tests that we got good holiday"""
        holi = compliments.getholidays()
        self.assertIsNotNone(holi)


if __name__ == "__main__":
    unittest.main()
