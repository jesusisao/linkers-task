import unittest
import csv
import json
from pprint import pprint

from constants import ADDRESS_CSV_PATH


class TestCsv(unittest.TestCase):

    @unittest.skip("test for investigation")
    def test_postcode_duplicate_count(self):
        """
        CSVには住所名が複数行にわたって書かれているものがある。
        その複数行の最大行数を調査するためのテスト。
        """
        postcode_count_dic = {}
        with open(ADDRESS_CSV_PATH, encoding='shift_jis') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                postcode = row[2]
                does_postcode_represent_two_or_more_towns = row[12] == '1'
                if does_postcode_represent_two_or_more_towns:
                    # 郵便番号が複数の町域を示すことがある区分。
                    # この場合は複数行としてカウントしないので、何もしない
                    continue
                if postcode_count_dic.get(postcode) is None:
                    postcode_count_dic[postcode] = 1
                else:
                    postcode_count_dic[postcode] += 1
        with open('tests/log/postcode_duplicate_count_log.txt', mode='w') as f:
            f.write(json.dumps(postcode_count_dic))
        actual = max(postcode_count_dic.values())
        # 最大で8行に渡って書かれた住所があった……
        self.assertEqual(8, actual)
