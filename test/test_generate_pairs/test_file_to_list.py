import os
import unittest
import generate_pairs


def expand_filename(filename):
    return os.path.join(os.path.dirname(__file__), filename)


class MyTestCase(unittest.TestCase):

    def test_empty(self):
        result = generate_pairs.file_to_list(expand_filename('empty.txt'))

        self.assertEqual([], result)

    def test_nonEmpty(self):
        result = generate_pairs.file_to_list(expand_filename('two.txt'))

        self.assertEqual(["one", "two"], result)
