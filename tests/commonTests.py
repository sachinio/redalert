__author__ = 'sachinpatney'

import unittest, sys

sys.path.append('/var/www/git/redalert/tasks')

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
        write_list_to_csv(['A','B','C'],['10', 20, {'complex': 'list'}])
        l = read_csv_as_list(CSV_TEST_FILE)
        self.assertEqual(l[1], '10')
        self.assertEqual(l[2]['complex'], 'list')

if __name__ == '__main__':
    unittest.main()