""" a test suite for all tests in compliments"""
import unittest
import compliments
import api_interface


class TestCompliments(unittest.TestCase):
    """ a test class to test all compliments """

    def testlist(self):
        """test the list function"""
        listresult = api_interface.getquotes()
        for l in listresult:
            print(l)
        self.assertIsNotNone(listresult)

    def testcompliment(self):
        """test the overall compliments"""
        compliments.compliment()
        complimentresult = compliments.compliment()
        self.assertIsNotNone(complimentresult)

    def testsummer(self):
        """test the summer compliment"""
        summer = api_interface.getsummer()
        self.assertIsNotNone(summer)

    def testkanye(self):
        """tests that we get the kanye compliment"""
        kanye = api_interface.getkanye()
        self.assertIsNotNone(kanye)
        self.assertNotEqual(kanye, "kanye is awesome")

    def testquote(self):
        """tests that we got a good quote"""
        quote = api_interface.getquote()
        self.assertIsNotNone(quote)
        self.assertNotEqual("dad quotes are cool", quote)

    def testtips(self):
        """ tests that we got a good tip"""
        tips = api_interface.gettips()
        self.assertIsNotNone(tips)

    def testholiday(self):
        """tests that we got good holiday"""
        holi = compliments.getholidays()
        self.assertIsNotNone(holi)


if __name__ == '__main__':
    unittest.main()
