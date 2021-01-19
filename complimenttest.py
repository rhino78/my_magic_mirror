import unittest
import compliments

class TestCompliments(unittest.TestCase):

    def testCompliment(self):
        v = compliments.compliment()
        covid = compliments.getCovid()
        stage = compliments.getStage()
        tips = compliments.getTips()
        holi = compliments.getHolidays()
        results = [v, covid, stage, tips, holi]
        self.assertEqual(5, len(results))
        self.assertIsNot(None, v)
        self.assertIsNot(None, stage)


if __name__ == '__main__':
    unittest.main()
