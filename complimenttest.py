import unittest
import compliments

class TestCompliments(unittest.TestCase):

    def testCompliment(self):
        v = compliments.compliment()
        self.assertIsNot(None, v)


if __name__ == '__main__':
    unittest.main()
