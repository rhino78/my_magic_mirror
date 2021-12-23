""" a tes suite for all tests in compliments"""
import unittest
import compliments
import api_interface


class TestCompliments(unittest.TestCase):
    """ a test class to test all compliments """

    def testlist(self):
        """test the list function"""
        listresult = api_interface.getquotes()
        self.assertIsNotNone(listresult)

    def testcompliment(self):
        """test the overall compliments"""
        complimentresult = compliments.compliment()
        self.assertIsNotNone(complimentresult)

    def testcovidstage(self):
        """tests the covid stage"""
        covidstage = api_interface.getstage()
        print("the covid stage is : {}".format(covidstage))
        print(covidstage)
        self.assertIsNotNone(covidstage)
        self.assertNotEqual("travis county is overrun by zombies", covidstage)

    def testcovid(self):
        """tests the covid compliment"""
        covid = api_interface.getcovid()
        self.assertIsNotNone(covid)

    def teststage(self):
        """test the current stage compliment"""
        stage = api_interface.getstage()
        print("the covid stage is: {}".format(stage))
        print(stage)
        self.assertIsNotNone(stage)

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

    def testmom(self):
        """tests that we got a good mom quote"""
        mom = api_interface.getyomomma()
        self.assertIsNotNone(mom)

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
