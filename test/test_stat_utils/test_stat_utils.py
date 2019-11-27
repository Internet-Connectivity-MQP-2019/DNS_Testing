import unittest
from stat_utils import generate_statistics, calculate_coefficient_of_variation


class MyTestCase(unittest.TestCase):
    def testEmptyList(self):
        self.assertEqual("NULL,NULL,NULL,NULL", generate_statistics([]))

    def testSingleElement(self):
        self.assertEqual("1.00,1.00,NULL,NULL", generate_statistics([1]))
        self.assertEqual("42.00,42.00,NULL,NULL", generate_statistics([42]))

    def testTwoElements(self):
        self.assertEqual("1.00,1.00,0.00,0.00", generate_statistics([1, 1]))
        self.assertEqual("1.50,1.50,0.71,0.50", generate_statistics([1, 2]))

    def testCalculateCoefficientOfVariation(self):
        # Numbers are from online calculator
        self.assertAlmostEqual(0.0733, calculate_coefficient_of_variation(4.5, 0.33), places=3)
        self.assertAlmostEqual(0.00733, calculate_coefficient_of_variation(45, 0.33), places=3)
        self.assertAlmostEqual(0.28571429, calculate_coefficient_of_variation(42, 12), places=3)
