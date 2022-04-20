""" a test suite for all tests in compliments"""
import unittest
import compliments
import api_interface


class TestCompliments(unittest.TestCase):
    """ a test class to test all compliments """

    def testlist(self):
        """test the list function"""
        listresult = api_interface.getquotes()
        test = [word for word in listresult if len(word) < 150]
        print(len(test))

        for t in test:
            print(len(t))
            print(t)

        print(len(listresult))
        self.assertIsNotNone(listresult)

    def testcompliment(self):
        """test the overall compliments"""
        complimentresult = compliments.compliment()
        self.assertIsNotNone(complimentresult)

    def testcovidstage(self):
        """tests the covid stage"""
        covidstage = api_interface.getstage()
        self.assertIsNotNone(covidstage)
        print("covid stage: ")
        print(covidstage)
        self.assertNotEqual("travis county is overrun by zombies", covidstage)

    # def testcovid2(self):
    #     covidstage = api_interface.getstagealt()
    #     self.assertIsNotNone(covidstage)
    #     print(covidstage)
    #     self.assertNotEqual("travis county is overrun by zombies", covidstage)

    def testcovid(self):
        """
        tests the covid compliment
        We do not expect to get COVID Sucks, Wear a Mask
        """
        covid = api_interface.getcovid()
        self.assertNotEqual("COVID sucks", covid[0])
        self.assertNotEqual("Wear a Mask", covid[1])
        self.assertIsNotNone(covid)

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
        self.assertNotEqual("yo momma is very fat", mom)

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
