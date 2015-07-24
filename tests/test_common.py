__author__ = 'sachinpatney'

import unittest
import sys
import ast
import os
import common

sys.path.append('../tasks')

from vso import VSO
from common import write_dictionary_to_csv
from common import read_csv_as_dictionary
from common import sync_write_list_to_csv
from common import read_csv_as_list
from common import safe_read_dictionary
from unittest.mock import MagicMock


CSV_TEST_FILE = 'test.csv'
TIMELINE_FILE = 'timeline.csv'


class TestCSVMethods(unittest.TestCase):
    def test_read_write_dictionary(self):
        write_dictionary_to_csv({'iam': 'happy'}, CSV_TEST_FILE)
        d = read_csv_as_dictionary(CSV_TEST_FILE)

        self.assertEqual(d['iam'], 'happy')

    def test_read_write_list(self):
        sync_write_list_to_csv(
            ['A', 'B', 'C'],
            [
                {'A': '20', 'B': 30, 'C': {'complex': 'iam'}},
                {'A': '20', 'B': 30, 'C': ['complex', 'you', 'are']}
            ], CSV_TEST_FILE, 'w')
        l = read_csv_as_list(CSV_TEST_FILE)

        self.assertEqual(len(l), 2)
        self.assertEqual(l[0]['A'], '20')
        self.assertEqual(l[0]['B'], '30')
        self.assertEqual(ast.literal_eval(l[0]['C'])['complex'], 'iam')
        self.assertEqual(ast.literal_eval(l[1]['C'])[1], 'you')

        os.remove(CSV_TEST_FILE)  # clean up

    def test_read_write_list_with_append(self):
        for i in range(5):
            sync_write_list_to_csv(['A', 'B'], [{'A': '20', 'B': 40}], CSV_TEST_FILE, 'a')
        l = read_csv_as_list(CSV_TEST_FILE)

        self.assertEqual(len(l), 5)

        os.remove(CSV_TEST_FILE)  # clean up

    def test_unsupported_operation_read_write_list(self):
        try:
            sync_write_list_to_csv(['A', 'B'], [{'A': '20', 'B': 40}], CSV_TEST_FILE, 'r')
        except:
            return
        self.fail('Should have throw an exception')


class TestSafeReadMethods(unittest.TestCase):
    def test_safe_read_dictionary(self):
        d = {}
        v = safe_read_dictionary(d, 'unknown_value')

        self.assertIsNone(v)


class TestVSO(unittest.TestCase):
    def test_get_builds_with_broken(self):
        morphine = VSO()
        morphine.is_broken = MagicMock(return_value=True)
        common.OPTIONS_FILE_PATH = 'temp.csv'  # gets password from here
        info = morphine.get_broken_master_builds(morphine.get_build_info())

        self.assertTrue(len(info) > 0)

    def test_get_builds_without_broken(self):
        morphine = VSO()
        morphine.is_broken = MagicMock(return_value=False)
        common.OPTIONS_FILE_PATH = 'temp.csv'  # gets password from here
        info = morphine.get_broken_master_builds(morphine.get_build_info())

        self.assertEqual(len(info), 0)

    def test_add_item(self):
        common.TMP_FOLDER_PATH = './'
        common.Timeline.add_item('Sachin', 'its friday', 'Woooooo', 'test.gif', 'fa-beer', 'warning')

        l = read_csv_as_list(TIMELINE_FILE)

        self.assertEqual(l[0]['name'], 'Sachin')
        self.assertEqual(l[0]['title'], 'its friday')
        self.assertEqual(l[0]['content'], 'Woooooo')
        self.assertEqual(l[0]['img'], '../../../uploads/sachin/test.gif')
        self.assertEqual(l[0]['icon'], 'fa-beer')
        self.assertEqual(l[0]['iconBackground'], 'warning')

        os.remove(TIMELINE_FILE)  # clean up

if __name__ == '__main__':
    unittest.main()