# インデックスファイルと、元の住所CSVから、検索したい住所を表示する

import json
import csv
import sys
import os
from typing import Dict, List, Optional, Set, NewType
from pprint import pprint

from create_index import create_index, is_the_end_of_an_address
from n_gram import to_n_gram
from error import AddressNotFoundError, UserInputError, AddressCsvNotFoundError
from constants import INDEX_PATH, ADDRESS_CSV_PATH


# CSVの行番号を示す型
LineNumber = NewType('LineNumber', int)


def safe_list_get(l: List, idx: int, default=None):
    try:
        return l[idx]
    except IndexError:
        return default


def search_address(search_str: Optional[str]) -> List[str]:
    if search_str is None or search_str == '':
        raise UserInputError('引数に検索文字列を入れて下さい。')
    
    # 全角スペース除去
    search_str_extracted = search_str.replace('　', '')

    if len(search_str_extracted) <= 1:
        raise UserInputError('1文字以下では検索できません。')

    search_n_gram_list: List[str] = to_n_gram(search_str_extracted, 2)
    
    if not os.path.isfile(INDEX_PATH):
        print('indexファイルが存在しないため、indexファイルの作成を行います。')
        create_index()

    with open(INDEX_PATH) as f:
        index_dic: Dict = json.loads(f.read())

    line_number_set_list: List[Set[LineNumber]] = []
    for search_char2 in search_n_gram_list:
        # ex. line_numbers = [101, 20001, 90521]
        line_numbers: Optional[List[LineNumber]] = index_dic.get(search_char2)
        if line_numbers is None:
            pass
        else:
            line_number_set_list.append(set(line_numbers))
    
    if len(line_number_set_list) == 0:
        raise AddressNotFoundError('検索結果はありません。')

    line_number_union: Set[LineNumber] = set.union(*line_number_set_list)

    if not os.path.isfile(ADDRESS_CSV_PATH):
        raise AddressCsvNotFoundError('住所のCSVファイルが指定ディレクトリに存在しません。')

    with open(ADDRESS_CSV_PATH, encoding='shift_jis') as csv_file:
        reader_obj: List = list(csv.reader(csv_file))

    result: List[str] = []
    for line_number in line_number_union:
        index = line_number - 1
        address_row = reader_obj[index]
        address_str = '"' + address_row[2] + '","' + address_row[6] + '","' + address_row[7] + '","'
        
        add_index = 0
        while True:
            address_str += reader_obj[index + add_index][8]
            if is_the_end_of_an_address(reader_obj, index + add_index):
                result.append(address_str + '"')
                break
            add_index += 1
    return result


def main() -> None:
    args = sys.argv
    command_name: Optional[str] = safe_list_get(args, 1)
    search_str: Optional[str] = safe_list_get(args, 2)

    if command_name is None:
        print('引数が不足しています。')
        return

    if command_name == 'index':
        print('indexの作成を行います。')
        create_index()
        return
    
    if command_name == 'search':
        try:
            addresses: List[str] = search_address(search_str)
            for address in addresses:
                print(address)
        except UserInputError as e:
            print(e)
        except AddressNotFoundError as e:
            print(e)
        return
    
    print('不正なコマンドです。')

main()
