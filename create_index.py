# csvファイルからインデックスファイルを作成する

import csv
import json
from typing import Dict, List, NewType

from n_gram import to_n_gram
from constants import INDEX_PATH, ADDRESS_CSV_PATH


# CSVの行番号を示す型
LineNumber = NewType('LineNumber', int)


def add_list_value_to_dict_safely(dic: Dict, key: str, val: int) -> None:
    """
    引数のDictに対して値を追加するための関数。
    引数dicに破壊的変更を加えるので注意。
    引数dicの形式は下記のようになっている想定。
    {
        key1: [4],
        key2: [1, 2, 3],
    }
    ここに整数の値を追加したり、新しいkvペアを増やしたりする。
    """
    if dic.get(key) is None:
        dic[key] = [val]
    elif val in dic[key]:
        pass
    else:
        dic[key].append(val)


def is_the_end_of_an_address(reader_obj, index):
    """
    今見ている住所の行が、同一の住所における最終行かを判定する。
    複数行に住所が別れている場合があるためこの判定が必要。
    """
    row = reader_obj[index]
    if row[12] == '1':
        # 郵便番号が複数の町域を示す特殊な住所
        return True
    try:
        next_row = reader_obj[index + 1]
        if row[2] == next_row[2]:
            return False
        else:
            return True
    except IndexError as e:
        return True


def format_csv_obj(reader_obj: List[List[str]]) -> Dict[LineNumber, str]:
    """
    CSVは複数行に住所が別れていることがある。
    例えば、〒602-8368は8行に分かれている。
    それを扱いやすくするのがこの関数の目的。
    返り値は辞書。keyは複数行住所の先頭の行番号で、valueはフルの住所名。
    """
    new_dic: Dict[LineNumber, List[str]] = {}
    is_the_head_of_an_address = True
    joined_address = ''
    line_number = 0
    for i, row in enumerate(reader_obj):
        if is_the_head_of_an_address:
            line_number = i + 1
            # ex. joined_address = '北海道札幌市北区あいの里四条'
            joined_address += row[6] + row[7] + row[8]
        else:
            joined_address += row[8]
        
        if is_the_end_of_an_address(reader_obj, i):
            new_dic[line_number] = joined_address

            is_the_head_of_an_address = True
            joined_address = ''
            line_number = 0
        else:
            is_the_head_of_an_address = False
    return new_dic


def create_index():
    print('Creating index file...')
    index_dic = {}
    with open(ADDRESS_CSV_PATH, encoding='shift_jis') as csv_file:
        reader_obj: List[List[str]] = list(csv.reader(csv_file))
        address_dic: [LineNumber, str] = format_csv_obj(reader_obj)
        
        for line_number, address_name in address_dic.items():
            n_gram_list = to_n_gram(address_name, 2)
            for char2 in n_gram_list:
                add_list_value_to_dict_safely(index_dic, char2, line_number)

    with open(INDEX_PATH, mode='w') as index_file:
        index_file.write(json.dumps(index_dic))
    print('Index file has been created.')
