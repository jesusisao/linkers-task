import unittest
from n_gram import to_n_gram

class TestNGram(unittest.TestCase):

    def test_n_gram_2(self):
        test_str = '札幌'
        expected = ['札幌']
        actual = to_n_gram(test_str, 2)
        self.assertEqual(expected, actual)
    
    def test_n_gram_14(self):
        test_str = '北海道札幌市北区あいの里四条'
        expected = ['北海','海道','道札','札幌','幌市','市北','北区','区あ','あい','いの','の里','里四','四条']
        actual = to_n_gram(test_str, 2)
        self.assertEqual(expected, actual)
