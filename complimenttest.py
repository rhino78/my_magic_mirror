""" a tes suite for all tests in compliments"""
import unittest
import compliments

class TestCompliments(unittest.TestCase):
    """ a test class to test all compliments """

    def testcompliment(self):
        """test the overall compliments"""
        complimentresult = compliments.compliment()
        self.assertIsNotNone(complimentresult)

    def testcovidstage(self):
        """tests the covid stage"""
        covidstage = compliments.getstage()
        self.assertIsNotNone(covidstage)

    def testcovid(self):
        """tests the covid compliment"""
        covid = compliments.getcovid()
        self.assertIsNotNone(covid)

    def teststage(self):
        """test the current stage compliment"""
        stage = compliments.getstage()
        self.assertIsNotNone(stage)

    def testsummer(self):
        """test the summer compliment"""
        summer = compliments.getsummer()
        self.assertIsNotNone(summer)

    def testkanye(self):
        """tests that we get the kanye compliment"""
        kanye = compliments.getkanye()
        self.assertIsNotNone(kanye)

    def testquote(self):
        """tests that we got a good quote"""
        quote = compliments.getquote()
        self.assertIsNotNone(quote)

    def testmom(self):
        """tests that we got a good mom quote"""
        mom = compliments.getyomomma()
        self.assertIsNotNone(mom)

    def testtips(self):
        """ tests that we got a good tip"""
        tips = compliments.gettips()
        self.assertIsNotNone(tips)

    def testholiday(self):
        """tests that we got good holiday"""
        holi = compliments.getholidays()
        self.assertIsNotNone(holi)


if __name__ == '__main__':
    unittest.main()
