__author__ = 'sachinpatney'

import unittest
import sys
import ast

sys.path.append('../tasks')

from common import write_dictionary_to_csv
from common import read_csv_as_dictionary
from common import write_list_to_csv
from common import read_csv_as_list

CSV_TEST_FILE = 'test.csv'


class TestCSVMethods(unittest.TestCase):
    def test_read_write_dictionary(self):
        write_dictionary_to_csv({'iam': 'happy'}, CSV_TEST_FILE)
        d = read_csv_as_dictionary(CSV_TEST_FILE)
        self.assertEqual(d['iam'], 'happy')

    def test_read_write_list(self):
        write_list_to_csv(
            ['A', 'B', 'C'],
            [
                {'A': '20', 'B': 30, 'C': {'complex': 'iam'}},
                {'A': '20', 'B': 30, 'C': ['complex', 'you', 'are']}
            ], CSV_TEST_FILE)
        l = read_csv_as_list(CSV_TEST_FILE)
        self.assertEqual(len(l), 2)
        self.assertEqual(l[0]['A'], '20')
        self.assertEqual(l[0]['B'], '30')
        self.assertEqual(ast.literal_eval(l[0]['C'])['complex'], 'iam')
        self.assertEqual(ast.literal_eval(l[1]['C'])[1], 'you')


if __name__ == '__main__':
    unittest.main()